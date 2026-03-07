# Dataset INTERGRAMTION-FEATURE_EXTRACTION
demo
# Feature Extraction Guide

## 1. Giới thiệu

Trong Computer Vision, ảnh không thể đưa trực tiếp vào các thuật toán Machine Learning thông thường.
Ta cần chuyển ảnh thành **vector số** đại diện cho nội dung của ảnh.

Quá trình này gọi là **Feature Extraction**.

Pipeline tổng quát:

```
Image
 ↓
Preprocessing
 ↓
CNN Model
 ↓
Feature Vector (Embedding)
 ↓
Machine Learning / Similarity / Clustering
```

Trong project này, chúng ta sử dụng **ResNet50** để trích xuất đặc trưng từ ảnh.

Model được huấn luyện trên dataset **ImageNet**.

---

# 2. Cấu trúc Dataset

Dataset được tổ chức theo dạng thư mục:

```
dataset/
 ├ images/
 │   ├ train/
 │   │   ├ daisy/
 │   │   ├ dandelion/
 │   │   ├ sunflower/
 │   │   ├ tulip/
 │   │   └ peach_blossom/
 │   │
 │   ├ val/
 │   └ test/
 │
 ├ metadata/
 └ dataset_index.csv
```

Ý nghĩa:

| Folder   | Mục đích           |
| -------- | ------------------ |
| train    | dữ liệu huấn luyện |
| val      | dữ liệu validation |
| test     | dữ liệu kiểm tra   |
| metadata | thông tin dataset  |

Mỗi thư mục con là **một class hoa**.

---

# 3. Feature Extraction là gì?

Feature Extraction là quá trình:

```
Image → Vector số
```

Ví dụ:

```
cat.jpg
↓
[0.12, 0.04, 1.22, 0.33, ...]
```

Vector này gọi là:

* **Feature vector**
* **Embedding**

Trong project này:

```
1 ảnh → vector 2048 chiều
```

---

# 4. Model sử dụng

Chúng ta dùng:

ResNet50

Đây là một CNN architecture nổi tiếng được giới thiệu trong paper:

```
Deep Residual Learning for Image Recognition
```

Ưu điểm:

* rất mạnh cho feature extraction
* pretrained trên ImageNet
* output feature vector chất lượng

---

# 5. Pipeline Feature Extraction

Pipeline của project:

```
Dataset Images
↓
Preprocessing
↓
ResNet50
↓
Feature Vector (2048)
↓
Save features
```

---

# 6. Preprocessing

Trước khi đưa ảnh vào model, cần xử lý:

```
Resize
ToTensor
Normalize
```

Ví dụ code:

```python
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])
```

Giải thích:

| Step      | Ý nghĩa                       |
| --------- | ----------------------------- |
| Resize    | đưa ảnh về 224x224            |
| ToTensor  | chuyển ảnh thành tensor       |
| Normalize | chuẩn hóa pixel theo ImageNet |

---

# 7. Feature Extraction Code

Ví dụ trích xuất feature từ một ảnh:

```python
import torch
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import torchvision.transforms as transforms

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)

model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])

img = Image.open("cat.jpg").convert("RGB")

img = transform(img)
img = img.unsqueeze(0)

with torch.no_grad():
    feature = model(img)

feature = feature.squeeze().numpy()
```

Output:

```
(2048,)
```

---

# 8. Feature Vector

Feature vector là:

```
[0.0, 0.029, 0.022, 0.0, 0.158, ...]
```

Ý nghĩa:

* mỗi số đại diện cho một pattern
* CNN đã học các pattern từ ImageNet

Ví dụ:

```
feature[0] → edge
feature[200] → texture
feature[800] → object part
```

---

# 9. Lưu Feature

Feature thường được lưu dạng:

### CSV

```
image_path,f0,f1,f2,...f2047
image1.jpg,0.1,0.2,0.3,...
```

### NumPy

```
features.npy
```

shape:

```
(number_of_images , 2048)
```

---

# 10. Ứng dụng của Feature Vector

Sau khi có feature vector, ta có thể:

### Image Similarity

```
query image
↓
extract feature
↓
compare với dataset
↓
find similar images
```

### Clustering

```
features
↓
KMeans
↓
group similar images
```

### Visualization

```
features
↓
PCA / t-SNE / UMAP
↓
2D visualization
```

---

# 11. Pipeline tổng thể của Project

```
Dataset
↓
Feature Extraction (ResNet50)
↓
Feature Matrix
↓
Machine Learning / Similarity
```

---

# 12. Kết luận

Feature Extraction là bước quan trọng trong Computer Vision.

Thay vì xử lý trực tiếp ảnh, chúng ta chuyển ảnh thành **vector đặc trưng** để:

* dễ xử lý
* giảm dimensionality
* áp dụng Machine Learning.

ResNet50 là một backbone phổ biến để thực hiện bước này.

