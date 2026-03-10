from email.mime import image
import json, os
from src.models.Image import Image
from src.utils.logger import logger
from typing import Optional

class MetadataManager:
    """
    Class dùng để xử lý metadata tương ứng. Khởi tạo bằng thư mục mà ta muốn lưu trữ các metadata.

    Bao gồm các phương thức:

        - Set một metadata
        - Thêm một metadata vào danh sách.
        - Xuất danh sách metadata đó ra file JSON
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.metadatas_list = []

    def set_a_record(self, source: str, flower_type: str, path: str, image_url: Optional[str] = None) -> Image:
        """
        Set một metadata, có thể không có URL của bức ảnh đó.

        :params: source: str: Nguồn gốc của ảnh.
        :params: flower_type: str: Loại hoa.
        :params: path: str: Nơi lưu trữ ảnh.
        :params: image_url: str | None: URL của bức ảnh.

        :returns: metadata: Image: Metadata của bức ảnh đó, bao gồm các trường thông tin trên.
        """
        return Image(source=source,
                     flower_type=flower_type,
                     image_url=image_url, 
                     path=path)
    
    def add_into_list(self, metadata: Image) -> None:
        """
        Thêm một metadata vào danh sách

        :params: metadata: Image
        """
        self.metadatas_list.append({'source': metadata.source,
                                    'flower_type': metadata.flower_type,
                                    'image_url': metadata.image_url if metadata.image_url else '',
                                    'path': metadata.path
                               })
        
    def json_export(self) -> None:
        """
        Xuất danh sách ra thư mục tương ứng dưới định dạng .JSON
        """
        parent_dir = os.path.dirname(self.folder_path)
        os.makedirs(parent_dir,exist_ok=True)
        with open(self.folder_path, 'w',encoding = 'utf-8') as f:
            json.dump(obj = self.metadatas_list,
                      fp = f,
                      ensure_ascii=False,
                      indent = 2)
            logger.info(msg=f'Đã xuất ra file JSON thành công. Nơi lưu file: {self.folder_path}')