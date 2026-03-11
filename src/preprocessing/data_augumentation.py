import cv2 #type:ignore
import numpy as np #type:ignore
import math
import random
from pathlib import Path

class ImageAugmentation:
    def __init__(self, target_size=(224, 224)):
        self.target_w, self.target_h = target_size

    def _get_affine_matrix(self, w, h, angle, tx, ty, sh_x, sh_y):
        """Tạo Siêu Ma Trận Affine 3x3 gộp Xoay, Tịnh tiến và Nghiêng
            Để lần lượt thực hiện Xoay -> Nghiêng -> Tịnh tiến thì p.trình được các ma trận biến đổi nhân lần lượt từ phải sang trái để ra được
            M_transform: Ma trận kết hợp
        """
        cx, cy = w / 2, h / 2
        theta = math.radians(angle)
        cos_t, sin_t = math.cos(theta), math.sin(theta)

        M_to_origin = np.array([[1, 0, -cx],
                                [0, 1, -cy],
                                [0, 0, 1]])
        M_transform = np.array([
            [cos_t + sh_x*sin_t, -sin_t + sh_x*cos_t, tx],
            [sin_t + sh_y*cos_t,  cos_t - sh_y*sin_t, ty],
            [0,                   0,                  1]
        ])
        M_back = np.array([[1, 0, cx], 
                           [0, 1, cy], 
                           [0, 0, 1]])
        
        return M_back.dot(M_transform).dot(M_to_origin)

    def execute_pipeline(self, image_path):
        """Chạy pipeline"""
        # Đọc ảnh và chuyển sang RGB
        img = cv2.imread(str(image_path))
        if img is None:
            return None, None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA) # Ép về khoảng 256x256
        h, w, c = img.shape

        angle = random.uniform(-30, 30) # Random tham số trong khoảng an toàn để không làm nát ảnh
        tx, ty = random.uniform(-15, 15), random.uniform(-15, 15)
        sh_x, sh_y = random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)

        M = self._get_affine_matrix(w, h, angle, tx, ty, sh_x, sh_y)
        
        img = cv2.warpAffine(img, M[:2, :], (w, h), borderValue=(0, 0, 0)) # Cắt bỏ hàng cuối của ma trận 3x3 thành 2x3

        # Random Crop
        if h >= self.target_h and w >= self.target_w:
            max_y = h - self.target_h
            max_x = w - self.target_w
            
            # Chọn ngẫu nhiên tọa độ góc trên bên trái
            start_y = random.randint(0, max_y)
            start_x = random.randint(0, max_x)
            
            img = img[start_y : start_y + self.target_h, start_x : start_x + self.target_w] # Cắt đúng size 224x224 ra
        else:# Fallback an toàn (Phòng hờ lọt ảnh nhỏ hơn 224x224 vào hệ thống)
            img = cv2.resize(img, (self.target_w, self.target_h), interpolation=cv2.INTER_AREA)

        # Resize/Scaling lại sau khi cắt
        img = cv2.resize(img, (self.target_w, self.target_h), interpolation=cv2.INTER_AREA)

        alpha = random.uniform(0.8, 1.2) # Tương phản
        beta = random.uniform(-20, 20)   # Độ sáng
        img = np.clip(alpha * img + beta, 0, 255)

        # Noise & Blurr
        if random.random() > 0.5: # 50% cơ hội bị làm mờ
            img = cv2.GaussianBlur(img, (3, 3), 0)
        if random.random() > 0.5: # 50% cơ hội bị dính nhiễu hạt
            noise = np.random.normal(0, 10, img.shape)
            img = np.clip(img + noise, 0, 255)

        preview_img = img.astype(np.uint8)
        return preview_img