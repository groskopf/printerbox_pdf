import os
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from werkzeug.utils import secure_filename

from details import Details
from file_path import FilePath
from printer_code import PrinterCode
from site_paths import labelsPath
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf import name_tag_sheet_456090

router = APIRouter()

def allFilesInLabels():
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(labelsPath, topdown=False):
        for name in foundFiles:
            files.append(FilePath(filename=os.path.join(root, name)))

    return files

@router.post('/',
             response_model=FilePath,
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": Details},
                 status.HTTP_404_NOT_FOUND: {"model": Details}
             })
def new_name_tag_sheet(name_tag_sheet_type: NameTagSheetType, layout: Layout, name_data_list: List[NameData]):
    outputFilename = labelsPath + name_tag_sheet_type + '_' + uuid4().hex + '.pdf'

    match name_tag_sheet_type:
        case NameTagSheetType._456090:
            name_tag_sheet_456090.create(
                outputFilename, layout, name_data_list)
        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="NameTagSheetType not supported")

    return FilePath(filename=outputFilename)


@router.get('/', response_model=List[FilePath])
def get_name_tag_sheets():
    return allFilesInLabels()


@router.get('/{filename}',
            response_model=FilePath,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_name_tag_sheet(filename : str):
    nameTagFilename = labelsPath + secure_filename(filename)
    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        os.remove(nameTagFilename)
        return FilePath(filename=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sheet not found")

@router.delete('/{filename}', 
            response_model=FilePath,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def delete_name_tag_sheet(filename: str):
    securedFileName = secure_filename(filename)
    nameTagFilename = labelsPath + os.path.basename(securedFileName)

    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        os.remove(nameTagFilename)
        return FilePath(filename=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Sheet not found")