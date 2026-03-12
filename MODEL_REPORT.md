# Báo cáo Đánh giá Mô hình Phân loại Hoa (Feature Store + SVM)

## 1. Tổng quan luồng dữ liệu (Data Pipeline)
Hệ thống đã nạp thành công dữ liệu từ Feature Store (`.npy` files) sinh ra bởi mạng ResNet50. 
- **Tổng số ảnh hợp lệ đưa vào train:** 3,238 ảnh.
- **Tỷ lệ phân chia (Train/Val/Test):** ~ 70% / 15% / 15%.
  - Tập Train: 2,263 mẫu
  - Tập Validation: 481 mẫu
  - Tập Test: 494 mẫu

## 2. Kiến trúc thuật toán
- **Giảm chiều dữ liệu (Dimensionality Reduction):** Sử dụng PCA ép vector từ 2048D xuống 128D để khử nhiễu.
- **Thuật toán Phân loại (Classifier):** Support Vector Machine (Kernel RBF, C=1.0).

## 3. Kết quả nghiệm thu (Model Performance)
Mô hình thể hiện sự ổn định tốt, không có hiện tượng Overfitting.
- **Validation Accuracy:** 86.28%
- **Test Accuracy (Thực tế):** 86.84%

### Bảng Điểm Chi Tiết Trên Tập Test (Classification Report)

| Loài hoa (Class) | Độ chính xác (Precision) | Độ phủ (Recall) | Điểm F1 (F1-Score) | Số lượng ảnh (Support) |
| :--- | :---: | :---: | :---: | :---: |
| **apricot_blossom** | 0.86 | 0.91 | 0.88 | 46 |
| **daisy** | 0.80 | 0.80 | 0.80 | 45 |
| **dandelion** | 0.91 | 0.84 | 0.88 | 51 |
| **hibiscus** | 0.92 | 0.89 | 0.91 | 55 |
| **hydrangea** | 0.84 | 0.93 | 0.88 | 60 |
| **orchid** | 0.82 | 0.86 | 0.84 | 49 |
| **peach_blossom** | 0.87 | 0.85 | 0.86 | 48 |
| **rose** | 0.81 | 0.84 | 0.83 | 45 |
| **sunflower** | 0.93 | 0.89 | 0.91 | 46 |
| **tulip** | 0.93 | 0.84 | 0.88 | 49 |
| **Tổng quan (Accuracy)** | | | **0.87** | **494** |
| *Trung bình cộng (Macro Avg)* | *0.87* | *0.87* | *0.87* | *494* |
| *Trung bình trọng số (Weighted Avg)* | *0.87* | *0.87* | *0.87* | *494* |

*Ghi chú đánh giá theo F1-Score:*
- **Nhóm Xuất sắc (F1 > 0.90):** Hibiscus, Sunflower.
- **Nhóm Khá (0.85 < F1 <= 0.90):** Apricot Blossom, Dandelion, Hydrangea, Peach Blossom, Tulip.
- **Nhóm Cần cải thiện (F1 <= 0.85):** Daisy, Rose, Orchid.