# Thu thập dữ liệu về các loài hoa

## Mục tiêu thu thập

- 3000 ảnh về các loài hoa khác nhau (Có thể mở rộng thêm)
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

## Nguồn thu thập hiện tại

- Google Image
- Kaggle

## Metadata tương ứng

```json
{
    "source": # Nguồn lấy ảnh,
    "flower_type": # Loài hoa,
    "image_url": # Link ảnh tương ứng,
    "path": # Đường dẫn đến ảnh
}
```

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

## Vấn đề gặp phải

- Khi cào ảnh từ Google Image về dễ bị dính phải CAPTCHA, số lượng cào trong một lượt tìm kiếm chỉ thu về được ~70-80 ảnh
