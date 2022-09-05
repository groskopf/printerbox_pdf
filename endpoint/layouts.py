import os
from typing import List
from fastapi import APIRouter, status, HTTPException, Security
from fastapi.security.api_key import APIKey
from pydantic import BaseModel
from details import Details
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf.name_tag_layouts import NameTagLayouts, nameTagLayoutsList, getNameTagLayouts
from pdf.sheet_type import SheetType
from pdf.sheet_layouts import SheetLayouts, sheetLayoutsList, getSheetLayouts

from site_paths import imagesPath
from endpoint.authentication import AccessScope, authenticate_api_key

router = APIRouter()


@router.get('/name_tags', response_model=List[NameTagLayouts])
def get_name_tag_layouts(api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    return nameTagLayoutsList


@router.get('/sheets', response_model=List[SheetLayouts])
def get_sheet_layouts(api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    return sheetLayoutsList


@router.get('/name_tags/{name_tag_type}',
            response_model=NameTagLayouts,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_image(name_tag_type: NameTagType, api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    nameTagLayouts = getNameTagLayouts(name_tag_type)

    if not nameTagLayouts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="Name tag type not found")

    return nameTagLayouts


@router.get('/sheets/{sheet_type}',
            response_model=SheetLayouts,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_image(sheet_type: SheetType, api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    sheetLayouts = getSheetLayouts(sheet_type)

    if not sheetLayouts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="Name tag sheet type not found")

    return sheetLayouts
