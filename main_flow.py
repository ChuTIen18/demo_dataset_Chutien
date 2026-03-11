import torch
import os
import numpy as np
import cv2
import math
import random
from pathlib import Path
from PIL import Image

from torchvision.models import resnet50, ResNet50_Weights
import torchvision.transforms as transforms


# ==================================================
# IMAGE AUGMENTATION
# ==================================================

class ImageAugmentation:

    def __init__(self, target_size=(224,224)):
        self.target_w, self.target_h = target_size

    def _get_affine_matrix(self, w, h, angle, tx, ty, sh_x, sh_y):

        cx, cy = w/2, h/2
        theta = math.radians(angle)

        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        M_to_origin = np.array([
            [1,0,-cx],
            [0,1,-cy],
            [0,0,1]
        ])

        M_transform = np.array([
            [cos_t + sh_x*sin_t, -sin_t + sh_x*cos_t, tx],
            [sin_t + sh_y*cos_t,  cos_t - sh_y*sin_t, ty],
            [0,0,1]
        ])

        M_back = np.array([
            [1,0,cx],
            [0,1,cy],
            [0,0,1]
        ])

        return M_back.dot(M_transform).dot(M_to_origin)


    def execute_pipeline(self, image_path):

        img = cv2.imread(str(image_path))
        if img is None:
            return None

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)

        img = cv2.resize(img,(256,256))
        h,w,c = img.shape

        angle = random.uniform(-30,30)
        tx = random.uniform(-15,15)
        ty = random.uniform(-15,15)

        sh_x = random.uniform(-0.1,0.1)
        sh_y = random.uniform(-0.1,0.1)

        M = self._get_affine_matrix(w,h,angle,tx,ty,sh_x,sh_y)

        img = cv2.warpAffine(img,M[:2,:],(w,h))

        # random crop
        if h>=224 and w>=224:

            max_y = h-224
            max_x = w-224

            start_y = random.randint(0,max_y)
            start_x = random.randint(0,max_x)

            img = img[start_y:start_y+224, start_x:start_x+224]

        img = cv2.resize(img,(224,224))

        alpha = random.uniform(0.8,1.2)
        beta = random.uniform(-20,20)

        img = np.clip(alpha*img + beta,0,255)

        if random.random()>0.5:
            img = cv2.GaussianBlur(img,(3,3),0)

        if random.random()>0.5:
            noise = np.random.normal(0,10,img.shape)
            img = np.clip(img+noise,0,255)

        return img.astype(np.uint8)


# ==================================================
# LOAD RESNET MODEL
# ==================================================

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)

model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()


# ==================================================
# TORCH TRANSFORM
# ==================================================

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])


# ==================================================
# DATASET
# ==================================================

dataset_path = "dataset/images"

augmenter = ImageAugmentation()

features = []
image_paths = []


# ==================================================
# PIPELINE
# ==================================================

for root,dirs,files in os.walk(dataset_path):

    for file in files:

        if file.lower().endswith((".jpg",".jpeg",".png")):

            img_path = os.path.join(root,file)

            try:

                # augmentation
                aug_img = augmenter.execute_pipeline(img_path)

                if aug_img is None:
                    continue

                # convert to PIL
                pil_img = Image.fromarray(aug_img)

                # tensor transform
                img_tensor = transform(pil_img)
                img_tensor = img_tensor.unsqueeze(0)

                # feature extraction
                with torch.no_grad():
                    feature = model(img_tensor)

                feature = feature.squeeze().numpy()

                features.append(feature)
                image_paths.append(img_path)

                print("processed:", img_path)

            except Exception as e:
                print("error:", img_path, e)


# ==================================================
# SAVE FEATURES
# ==================================================

features = np.array(features)
image_paths = np.array(image_paths)

np.save("features.npy",features)
np.save("image_paths.npy",image_paths)

print("\nDONE")
print("features shape:",features.shape)