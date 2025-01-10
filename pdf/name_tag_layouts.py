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
        layouts=[Layout.LAYOUT_1,
                 Layout.LAYOUT_2,
                 Layout.LAYOUT_2PT,
                 Layout.LAYOUT_2PB,
                 Layout.LAYOUT_2PTL,
                 Layout.LAYOUT_2PTR,
                 Layout.LAYOUT_2PBL,
                 Layout.LAYOUT_2PBR,
                 Layout.LAYOUT_3,
                 Layout.LAYOUT_3PT,
                 Layout.LAYOUT_3PB,
                 Layout.LAYOUT_3PTL,
                 Layout.LAYOUT_3PTR,
                 Layout.LAYOUT_3PBL,
                 Layout.LAYOUT_3PBR
                 ]
    ),
    NameTagLayouts(
        name_tag_type=NameTagType._4786103,
        layouts=[Layout.LAYOUT_1,
                 Layout.LAYOUT_2,
                 Layout.LAYOUT_2PT,
                 Layout.LAYOUT_2PB,
                 Layout.LAYOUT_2PTL,
                 Layout.LAYOUT_2PTR,
                 Layout.LAYOUT_2PBL,
                 Layout.LAYOUT_2PBR,
                 Layout.LAYOUT_3,
                 Layout.LAYOUT_3PT,
                 Layout.LAYOUT_3PB,
                 Layout.LAYOUT_3PTL,
                 Layout.LAYOUT_3PTR,
                 Layout.LAYOUT_3PBL,
                 Layout.LAYOUT_3PBR
                 ]
    ),
]


def getNameTagLayouts(nameTagType: NameTagType) -> None | NameTagLayouts:
    for nameTagLayouts in nameTagLayoutsList:
        if nameTagLayouts.name_tag_type == nameTagType:
            return nameTagLayouts
    return None
