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
                 Layout.LAYOUT_2QT,
                 Layout.LAYOUT_2QB,
                 Layout.LAYOUT_2QTL,
                 Layout.LAYOUT_2QTR,
                 Layout.LAYOUT_2QBL,
                 Layout.LAYOUT_2QBR,
                 Layout.LAYOUT_2PTLQ,
                 Layout.LAYOUT_2PTRQ,
                 Layout.LAYOUT_2PBLQ,
                 Layout.LAYOUT_2PBRQ,
                 Layout.LAYOUT_3,
                 Layout.LAYOUT_3PT,
                 Layout.LAYOUT_3PB,
                 Layout.LAYOUT_3PTL,
                 Layout.LAYOUT_3PTR,
                 Layout.LAYOUT_3PBL,
                 Layout.LAYOUT_3PBR,
                 Layout.LAYOUT_3PTLQ,
                 Layout.LAYOUT_3PTRQ,
                 Layout.LAYOUT_3PBLQ,
                 Layout.LAYOUT_3PBRQ,
                 Layout.LAYOUT_3QT,
                 Layout.LAYOUT_3QB,
                 Layout.LAYOUT_3QTL,
                 Layout.LAYOUT_3QTR,
                 Layout.LAYOUT_3QBL,
                 Layout.LAYOUT_3QBR
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
                 Layout.LAYOUT_2QT,
                 Layout.LAYOUT_2QB,
                 Layout.LAYOUT_2QTL,
                 Layout.LAYOUT_2QTR,
                 Layout.LAYOUT_2QBL,
                 Layout.LAYOUT_2QBR,
                 Layout.LAYOUT_2PTLQ,
                 Layout.LAYOUT_2PTRQ,
                 Layout.LAYOUT_2PBLQ,
                 Layout.LAYOUT_2PBRQ,
                 Layout.LAYOUT_3,
                 Layout.LAYOUT_3PT,
                 Layout.LAYOUT_3PB,
                 Layout.LAYOUT_3PTL,
                 Layout.LAYOUT_3PTR,
                 Layout.LAYOUT_3PBL,
                 Layout.LAYOUT_3PBR,
                 Layout.LAYOUT_3PTLQ,
                 Layout.LAYOUT_3PTRQ,
                 Layout.LAYOUT_3PBLQ,
                 Layout.LAYOUT_3PBRQ,
                 Layout.LAYOUT_3QT,
                 Layout.LAYOUT_3QB,
                 Layout.LAYOUT_3QTL,
                 Layout.LAYOUT_3QTR,
                 Layout.LAYOUT_3QBL,
                 Layout.LAYOUT_3QBR
                 ]
    ),
]


def getNameTagLayouts(nameTagType: NameTagType) -> None | NameTagLayouts:
    for nameTagLayouts in nameTagLayoutsList:
        if nameTagLayouts.name_tag_type == nameTagType:
            return nameTagLayouts
    return None
