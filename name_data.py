from typing import Optional
from pydantic import BaseModel

class NameData(BaseModel):
    line_1: str
    line_2: Optional[str] = None
    line_3: Optional[str] = None
    line_4: Optional[str] = None
    line_5: Optional[str] = None
    image_name: Optional[str] = None
    qr_code: Optional[str] = None
    