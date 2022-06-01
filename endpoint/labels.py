import os
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from werkzeug.utils import secure_filename

from details import Details
from file_path import FilePath
from pdf.sheet_layouts import getSheetLayouts
from printer_code import PrinterCode
from site_paths import labelsPath
from name_data import NameData
from pdf.layouts import Layout
from pdf.sheet_type import SheetType
from pdf import sheet_456090

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
def new_sheet(sheet_type: SheetType, layout: Layout, name_data_list: List[NameData]):
    outputFilename = labelsPath + sheet_type + '_' + uuid4().hex + '.pdf'

    if layout not in getSheetLayouts(sheet_type).layouts:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, detail="Name tag sheet layout not supported")

    match sheet_type:
        case SheetType._456090:
            sheet_456090.create(
                outputFilename, layout, name_data_list)
        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Name tag sheet type not supported")

    return FilePath(filename=outputFilename)


@router.get('/', response_model=List[FilePath])
def get_sheets():
    return allFilesInLabels()


@router.get('/{filename}',
            response_class=FileResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_sheet(filename: str):
    nameTagFilename = labelsPath + secure_filename(filename)
    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        return FileResponse(path=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Sheet not found")


@router.delete('/{filename}',
               response_model=FilePath,
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": Details},
               })
def delete_sheet(filename: str):
    securedFileName = secure_filename(filename)
    nameTagFilename = labelsPath + os.path.basename(securedFileName)

    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        os.remove(nameTagFilename)
        return FilePath(filename=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Sheet not found")
