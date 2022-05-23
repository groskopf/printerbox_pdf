import os
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from endpoint.printerbox import Filename

from filePaths import labelsPath
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf import name_tag_sheet_456090

router = APIRouter()

@router.post('/{name_tag_sheet_type}/{layout}', response_model=Filename, status_code=status.HTTP_201_CREATED)
def nameTagSheet(name_tag_sheet_type : NameTagSheetType, layout : Layout, name_data_list: List[NameData]):
    outputFilename = labelsPath + name_tag_sheet_type + '_' + uuid4().hex + '.pdf'

    match name_tag_sheet_type:
        case NameTagSheetType._456090:
            name_tag_sheet_456090.create(outputFilename, layout, name_data_list)
        case _:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NameTagSheetType not supported")

    return Filename(filename=outputFilename)
