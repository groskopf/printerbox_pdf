import os
from typing import List
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from details import Details
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf.name_tag_sheet_type import NameTagSheetType

from site_paths import imagesPath

router = APIRouter()


class NameTagLayouts(BaseModel):
    name_tag_type: NameTagType
    layouts: List[Layout]


class NameTagSheetLayouts(BaseModel):
    name_tag_sheet_type: NameTagSheetType
    layouts: List[Layout]


nameTagLayoutsList: List[NameTagLayouts] = [
    NameTagLayouts(
        name_tag_type=NameTagType._47150106,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagLayouts(
        name_tag_type=NameTagType._4760100,
        layouts=[Layout.LAYOUT_1]
    ),
    NameTagLayouts(
        name_tag_type=NameTagType._4786103,
        layouts=[Layout.LAYOUT_1]
    ),
]

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


@router.get('/name_tags', response_model=List[NameTagLayouts])
def get_name_tag_layouts():
    return nameTagLayoutsList


@router.get('/name_tags_sheets', response_model=List[NameTagSheetLayouts])
def get_name_tag_sheet_layouts():
    return nameTagSheetLayoutsList


@router.get('/name_tags/{name_tag_type}',
            response_model=NameTagLayouts,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_image(name_tag_type: NameTagType):
    nameTagLayouts = next(
        (nameTagLayouts for nameTagLayouts in nameTagLayoutsList if nameTagLayouts.name_tag_type == name_tag_type), None)

    if not nameTagLayouts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="Name tag type not found")

    return nameTagLayouts


@router.get('/name_tag_sheets/{name_tag_sheet_type}',
            response_model=NameTagSheetLayouts,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_image(name_tag_sheet_type: NameTagSheetType):
    nameTagSheetLayouts = next(
        (nameTagSheetLayouts for nameTagSheetLayouts in nameTagSheetLayoutsList if nameTagSheetLayouts.name_tag_sheet_type == name_tag_sheet_type), None)

    if not nameTagSheetLayouts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="Name tag sheet type not found")

    return nameTagSheetLayouts
