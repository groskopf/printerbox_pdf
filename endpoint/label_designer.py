import os
from typing import List
from uuid import uuid4
from fastapi import APIRouter, status

from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf import name_tag_sheet_456090

router = APIRouter()

@router.post('/{nameTagSheetType}/{layout}', status_code=status.HTTP_201_CREATED)
def nameTagSheet(nameTagSheetType : NameTagSheetType, layout : Layout, nameDataList: List[NameData]):
    path = 'label' + '/'
    filename = nameTagSheetType + '_' + uuid4().hex + '.pdf'

    if not os.path.exists(path):
        os.makedirs(path)

    match nameTagSheetType:
        case NameTagSheetType._456090:
            name_tag_sheet_456090.create(filename, layout, nameDataList)
        case _:
            filename = None

    return { "file_name" : filename}
