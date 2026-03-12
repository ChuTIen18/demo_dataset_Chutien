# Image Feature Extraction Pipeline Notes

## Overview

Sau khi chạy pipeline trích xuất đặc trưng bằng ResNet50, hệ thống sẽ
sinh ra 3 file chính:

-   `features.npy`
-   `image_paths.npy`
-   `splits.npy`

Ba file này có **cùng số lượng phần tử và cùng thứ tự index**, nghĩa là:

    index i của cả 3 file đều tương ứng cùng một ảnh

------------------------------------------------------------------------

# 1. features.npy

`features.npy` chứa **vector đặc trưng (feature vector)** của ảnh được
trích xuất bởi CNN.

Pipeline:

    Image → ResNet50 → Feature Vector (2048 chiều)

Ví dụ shape:

    features.shape = (5000, 2048)

Ý nghĩa:

-   **5000** → số lượng ảnh
-   **2048** → số đặc trưng do ResNet50 sinh ra

Ví dụ một vector:

    features[0] =
    [0.0021, 1.33, 0.54, 0.0001, ..., 0.89]

CNN đã biến ảnh thành **dữ liệu số để ML model xử lý**.

------------------------------------------------------------------------

# 2. image_paths.npy

File này lưu **đường dẫn tới ảnh gốc trong dataset**.

Ví dụ:

    dataset/images/train/tulip/tulip001.jpg
    dataset/images/train/tulip/tulip002.jpg
    dataset/images/val/rose/rose001.jpg
    dataset/images/test/daisy/daisy002.jpg

Mục đích:

-   truy ngược lại ảnh gốc
-   debug dataset
-   visualize prediction
-   kiểm tra lỗi model

------------------------------------------------------------------------

# 3. splits.npy

File này cho biết **ảnh thuộc tập nào**:

    train
    val
    test

Ví dụ:

    train
    train
    val
    test

Điều này giúp:

-   tách dữ liệu train / validation / test
-   tránh data leakage

------------------------------------------------------------------------

# 4. Quan hệ giữa 3 file

Ví dụ:

    index = 15

    features[15]    → vector CNN
    image_paths[15] → đường dẫn ảnh
    splits[15]      → train / val / test

Ví dụ:

    features[15] = [0.13, 0.55, ..., 1.03]
    image_paths[15] = dataset/images/train/tulip/tulip015.jpg
    splits[15] = train

Nghĩa là:

    ảnh tulip015.jpg
    thuộc tập train
    vector đặc trưng = features[15]

------------------------------------------------------------------------

# 5. Pipeline hoàn chỉnh

    dataset/images
         │
         ├── train
         ├── val
         └── test
                │
                ▼
    Image Augmentation
                ▼
    Tensor Transform
                ▼
    ResNet50 Feature Extraction
                ▼
    Feature Vector (2048)
                ▼
    features.npy
    image_paths.npy
    splits.npy

------------------------------------------------------------------------

# 6. Cách load lại dữ liệu

Ví dụ trong Python:

``` python
import numpy as np

features = np.load("features.npy")
paths = np.load("image_paths.npy")
splits = np.load("splits.npy")
```

Lọc dữ liệu train:

``` python
train_mask = splits == "train"
X_train = features[train_mask]
```

------------------------------------------------------------------------

# 7. File nên có thêm trong pipeline

Pipeline chuẩn thường thêm:

    labels.npy

Ví dụ:

    tulip
    tulip
    rose
    daisy

Khi đó dataset ML sẽ có dạng:

    X = features (2048)
    y = labels

Có thể train các model:

-   SVM
-   RandomForest
-   XGBoost
-   Logistic Regression

------------------------------------------------------------------------

# 8. Ý nghĩa trong ML Pipeline

Pipeline tổng thể:

    Image Dataset
          ↓
    Data Augmentation
          ↓
    CNN Feature Extraction
          ↓
    Numerical Dataset
          ↓
    Machine Learning Model

Bước hiện tại chính là:

    Feature Engineering cho dữ liệu ảnh
