'''
Created on 10. maj 2022

@author: paul
'''

from typing import Optional
from pydantic import BaseModel

class NameData(BaseModel):
    name: str
    description1: Optional[str] = None
    description2: Optional[str] = None
    description3: Optional[str] = None
    description4: Optional[str] = None
    imageName: Optional[str] = None
    