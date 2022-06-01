from typing import List
from pydantic import BaseModel

from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType


class NameTagLayouts(BaseModel):
    name_tag_type: NameTagType
    layouts: List[Layout]


nameTagLayoutsList: List[NameTagLayouts] = [
    NameTagLayouts(
        name_tag_type=NameTagType._4760100,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagLayouts(
        name_tag_type=NameTagType._4786103,
        layouts=[Layout.LAYOUT_1]
    ),
]


def getNameTagLayouts(nameTagType : NameTagLayouts):
    nameTagLayouts = next(
        (nameTagLayouts for nameTagLayouts in nameTagLayoutsList if nameTagLayouts.name_tag_type == nameTagType), None)
    return nameTagLayouts