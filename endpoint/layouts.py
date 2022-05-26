import os
from typing import List
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from details import Details
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf.name_tag_layouts import NameTagLayouts, nameTagLayoutsList, getNameTagLayouts
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf.name_tag_sheet_layouts import NameTagSheetLayouts, nameTagSheetLayoutsList, getNameTagSheetLayouts

from site_paths import imagesPath

router = APIRouter()


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
    nameTagLayouts = getNameTagLayouts(name_tag_type)

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
    nameTagSheetLayouts = getNameTagSheetLayouts(name_tag_sheet_type)
    
    if not nameTagSheetLayouts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="Name tag sheet type not found")

    return nameTagSheetLayouts
