import os
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status

from filePaths import labelsPath
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf import name_tag_sheet_456090

router = APIRouter()

@router.post('/{nameTagSheetType}/{layout}', status_code=status.HTTP_201_CREATED)
def nameTagSheet(nameTagSheetType : NameTagSheetType, layout : Layout, nameDataList: List[NameData]):
    outputFilename = labelsPath + nameTagSheetType + '_' + uuid4().hex + '.pdf'

    match nameTagSheetType:
        case NameTagSheetType._456090:
            name_tag_sheet_456090.create(outputFilename, layout, nameDataList)
        case _:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NameTagSheetType not supported")

    return {"filename": outputFilename}
