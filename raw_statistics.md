# Thu thập dữ liệu về các loài hoa

## Mục tiêu thu thập

- **3000** ảnh về các loài hoa khác nhau (Có thể mở rộng thêm)
- Có 10 loài hoa chính:
    + Hoa mai (apricot_blossom)
    + Hoa hồng (rose)
    + Hoa dâm bụt (hibiscus)
    + Hoa hướng dương (sunflower)
    + Hoa đào (peach_blossom)
    + Hoa cúc (daisy)
    + Hoa cẩm tú cầu (hydrangea) 
    + Hoa lan (orchid)
    + Hoa tulip
    + Hoa bồ công anh (dandelion)

## Yêu cầu kích thước

- Định dạng ảnh ưu tiên JPEG hoặc PNG.
- Kích cỡ tối thiểu không nhỏ hơn **320x320** px và không lớn hơn **1024x1024** px.
- Nếu ảnh lớn hơn **1024x1024** px thì resize lại về 1024 px.

## Định dạng metadata 

```json
{
    "source": # Nguồn lấy ảnh,
    "flower_type": # Loài hoa,
    "image_url": # Link ảnh tương ứng, có thể ảnh sẽ không có image_url nên trường này là Optional,
    "path": # Đường dẫn đến ảnh
}
```

## Luồng thu thập ảnh thô và resize chúng

Trong [main.py](main.py), tiền xử lý dữ liệu ảnh được thực hiện theo luồng sau:

### Đối với những nguồn ảnh được thu thập trực tiếp từ URL

1. Thu thập danh sách URL ảnh từ một trang nguồn bằng hàm `executing_script(url_to_access)`.
2. Khởi tạo bộ quản lý metadata `MetadataManager` để lưu thông tin ảnh vào file JSON.
3. Duyệt từng URL ảnh, sau đó khởi tạo `ImageProcessor(320, 1024)` để áp dụng chuẩn kích thước.
4. Tải ảnh từ URL và xử lý ảnh thông qua `processor.with_url(url, new_file_path)`:
    - Ảnh nhỏ hơn ngưỡng tối thiểu sẽ được loại bỏ.
    - Ảnh vượt quá ngưỡng tối đa sẽ được resize để đưa về phạm vi kích thước cho phép.
    - Ảnh hợp lệ được lưu vào thư mục đích với tên chuẩn hóa theo loài hoa và chỉ số.
5. Tạo metadata cho từng ảnh gồm `source`, `flower_type`, `image_url`, `path`, rồi thêm vào danh sách.
6. Sau khi xử lý xong toàn bộ ảnh, xuất metadata ra file JSON bằng `management.json_export()`.

### Đối với những nguồn ảnh được thu thập bằng cách tải về trước

1. Duyệt file path của ảnh cần chuyển đổi, trong quá trình duyệt sử dụng phương thức `processor.with_file(input_file_path, new_file_path)`:
    - Ảnh nhỏ hơn ngưỡng tối thiểu sẽ được giữ nguyên trong file path ban đầu (`input_file_path`).
    - Ảnh vượt quá ngưỡng tối đa sẽ được resize để đưa về phạm vi kích thước cho phép.
    - Ảnh hợp lệ được lưu vào thư mục đích với tên chuẩn hóa theo loài hoa và chỉ số.
2. Tạo metadata cho từng ảnh gồm `source`, `flower_type`, `path`, rồi thêm vào danh sách.
3. Sau khi xử lý xong toàn bộ ảnh, xuất metadata ra file JSON bằng `management.json_export()`.

Luồng này giúp dữ liệu đầu vào được đồng nhất về kích thước, dễ truy vết nguồn ảnh, và thuận tiện cho các bước huấn luyện mô hình sau này.

## Số lượng hiện tại

- Số loài hoa đã thu thập: 10
- Tổng cộng các ảnh về hoa thu được: 3234

| Loài hoa        | Số lượng |
|-----------------|----------|
| apricot_blossom | 303      |
| daisy           | 300      |
| dandelion       | 330      |
| hibiscus        | 359      |
| hydrangea       | 395      |
| orchid          | 318      |
| peach_blossom   | 313      |
| rose            | 300      |
| sunflower       | 302      |
| tulip           | 318      |

### Các biểu đồ thống kê số lượng

#### Thống kê loài hoa 

![Số lượng các loài hoa](/report/flower_type_bar_plot.png)

#### Thống kê các nguồn thu thập

![Các nguồn thu thập](/report/source_bar_plot.png)

## Vấn đề gặp phải

- Khi cào ảnh từ Google Image về dễ bị dính phải CAPTCHA, số lượng cào trong một lượt tìm kiếm chỉ thu về được ~70-80 ảnh
