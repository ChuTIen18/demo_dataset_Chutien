from PIL import Image
from io import BytesIO
from typing import Optional
from src.utils.logger import logger
import os, requests

class ImageProcessor:
    
    """
    Dùng để xử lý ảnh thu thập từ URL, hoặc từ đọc file ảnh
    """

    def __init__(self, min_size: int, max_size: int):
        """
        Khởi tạo class với kích cỡ tối thiểu, và kích cỡ tối đa
        """
        self.min_size = min_size
        self.max_size = max_size
    
    def _resizing_image(self, image: Image) -> Optional[Image.Image]:

        """
        Logic điều chỉnh kích cỡ của ảnh

        :params: Image: File ảnh đã được đọc từ URL hoặc từ file
        :returns: Image | None: Ảnh đã được điều chỉnh kích cỡ nếu > max_size, loại bỏ ảnh nếu có kích cỡ < min_size.
        """

        width, height = image.size
        if width < self.min_size or height < self.min_size:
            logger.info(msg = f'Ảnh có kích thước bé hơn {self.min_size}')
            return None
        else:
            if width > self.max_size or height > self.max_size:
                ratio = self.max_size / max(width, height)
                new_height, new_width = int(height * ratio), int(width * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(msg=f'Đã điều chỉnh kích cỡ ảnh về {new_width}x{new_height}px')
            
            return image
        
    def _downloading_image(self, image_content: Image, save_path: str) -> None:
        try:
            os.makedirs(os.path.dirname(save_path),exist_ok=True)
            image_content.save(save_path, 'JPEG')
            logger.info(msg='Đã tải ảnh về thành công')
        except Exception as e:
            logger.error(msg = f'Đã gặp lỗi trong quá trình tải ảnh về. Chi tiết: {e}')

    def with_file(self, image_path: str, new_image_path: Optional[str]) -> None:
        try:
            if os.path.exists(image_path):
                with Image.open(image_path) as image:
                    image = self._resizing_image(image)
                    if image:
                        if image.mode in ('RGBA','P'):
                            image = image.convert('RGB')

                        parent_dir = os.path.dirname(new_image_path)
                        os.makedirs(parent_dir, exist_ok=True)
                
                        self._downloading_image(image, new_image_path)

                        logger.info(msg = f'Đã chuyển file ảnh sang thư mục mới: {new_image_path}')
                    else:
                        logger.warning(msg = f'Không chuyển ảnh qua được thư mục mới')

        except Exception as e:
            logger.error(msg = f'Đã gặp lỗi. Chi tiết: {e}')


    def with_url(self, image_url: str, save_path: str) -> None:
        response = requests.get(image_url,stream=True)
        if response.status_code != 200:
            logger.error(msg=f'Không thể truy cập vào URL. Status code: {response.status_code}')
            return None
    
        else:
            try:
                img = Image.open(BytesIO(response.content))

                if img.mode in ('RGBA','P'):
                    img = img.convert('RGB')
                img = self._resizing_image(img)
                if img:
                    logger.info(msg='Ảnh hợp lệ')
                    self._downloading_image(img, save_path)
                    
                else:
                    logger.error(msg='Ảnh không đạt yêu cầu')
                    return None
                
            except Exception as e:
                logger.error(msg = f'Đã gặp lỗi: {e}')
                return None
