from typing import List
from pydantic import BaseModel

from pdf.layouts import Layout
from pdf.sheet_type import SheetType


class SheetLayouts(BaseModel):
    sheet_type: SheetType
    layouts: List[Layout]


sheetLayoutsList: List[SheetLayouts] = [
    SheetLayouts(
        sheet_type=SheetType._453060,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._454070,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._454075,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._454080,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._454880,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._4551105,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._455180,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._4560105,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._456090,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._4560105,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._4574105,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._463770,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._464764,
        layouts=[Layout.LAYOUT_1]
    ),
    SheetLayouts(
        sheet_type=SheetType._4669100,
        layouts=[Layout.LAYOUT_1]
    ),
]


def getSheetLayouts(sheetType : SheetType):
    sheetLayouts = next(
        (sheetLayouts for sheetLayouts in sheetLayoutsList if sheetLayouts.sheet_type == sheetType), None)
    return sheetLayouts