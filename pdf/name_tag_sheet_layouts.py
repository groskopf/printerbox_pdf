from typing import List
from pydantic import BaseModel

from pdf.layouts import Layout
from pdf.name_tag_sheet_type import NameTagSheetType


class NameTagSheetLayouts(BaseModel):
    name_tag_sheet_type: NameTagSheetType
    layouts: List[Layout]


nameTagSheetLayoutsList: List[NameTagSheetLayouts] = [
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._453060,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._454070,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._454075,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._454080,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._454880,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._4551105,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._455180,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._4560105,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._456090,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._4560105,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._4574105,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._463770,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._464764,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagSheetLayouts(
        name_tag_sheet_type=NameTagSheetType._4669100,
        layouts=[Layout.LAYOUT_1]
    ),
]


def getNameTagSheetLayouts(nameTagSheetType : NameTagSheetType):
    nameTagSheetLayouts = next(
        (nameTagSheetLayouts for nameTagSheetLayouts in nameTagSheetLayoutsList if nameTagSheetLayouts.name_tag_sheet_type == nameTagSheetType), None)
    return nameTagSheetLayouts