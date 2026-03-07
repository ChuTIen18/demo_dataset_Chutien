import torch
import os
import numpy as np
from PIL import Image
from torchvision.models import resnet50, ResNet50_Weights
import torchvision.transforms as transforms

# ==============================
# LOAD MODEL
# ==============================

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)

# remove classification layer
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# ==============================
# IMAGE PREPROCESSING
# ==============================

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

# ==============================
# DATASET PATH
# ==============================

dataset_path = "dataset/images"

features = []
image_paths = []

# ==============================
# LOOP THROUGH DATASET
# ==============================

for root, dirs, files in os.walk(dataset_path):

    for file in files:

        if file.lower().endswith((".jpg",".jpeg",".png")):

            img_path = os.path.join(root,file)

            try:

                img = Image.open(img_path).convert("RGB")
                img = transform(img)
                img = img.unsqueeze(0)

                with torch.no_grad():
                    feature = model(img)

                feature = feature.squeeze().numpy()

                features.append(feature)
                image_paths.append(img_path)

                print("processed:", img_path)

            except Exception as e:

                print("error:", img_path, e)

# ==============================
# CONVERT TO NUMPY
# ==============================

features = np.array(features)
image_paths = np.array(image_paths)

# ==============================
# SAVE FILES
# ==============================

np.save("features.npy", features)
np.save("image_paths.npy", image_paths)

print("\nDONE")
print("features shape:", features.shape)
print("paths shape:", image_paths.shape)