from pydantic import BaseModel
from typing import Optional

class Image(BaseModel):
    source: str
    flower_type: str
    image_url: Optional[str] = None
    path: str