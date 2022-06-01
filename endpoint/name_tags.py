import os
from typing import List
from uuid import uuid4
from datetime import date as date
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from werkzeug.utils import secure_filename

from details import Details
from pdf.name_tag_layouts import getNameTagLayouts
from site_paths import imagesPath, nameTagsPath
from printer_code import PrinterCode
from endpoint.bookings import calendar
from endpoint.bookings import Booking
from endpoint.name_tags_ws import getFilesInPrinterQueue, deleteFilesInPrinterQueue, wsConnectionManager, router
from file_path import FilePath
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf import name_tag_4786103

def checkImageFileExist(nameData: NameData):
    imageName = imagesPath + nameData.image_name
    if imageName:
        if not os.path.exists(imageName) or not os.path.isfile(imageName):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


def findBooking(bookingCode):
    booking: Booking = calendar.getBooking(bookingCode)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    today = date.today()  # FIXME today is not working correctly 
    if booking.start_date > today or today > booking.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Booking not valid today")
    return booking.printer_code, booking.name_tag_type


@router.post('/',
             response_model=FilePath,
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": Details},
                 status.HTTP_404_NOT_FOUND: {"model": Details}
             })
async def new_name_tag(booking_code: str, layout : Layout, name_data: NameData):
    name_data.image_name = secure_filename(name_data.image_name)
    checkImageFileExist(name_data)

    printerCode, nameTagType = findBooking(booking_code)

    if layout not in getNameTagLayouts(nameTagType).layouts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name tag layout not supported")

    outputPath = nameTagsPath + printerCode + '/'
    outputFilename = outputPath + nameTagType + '_' + uuid4().hex + '.pdf'

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    match nameTagType:
        case NameTagType._4786103:
            name_tag_4786103.create(outputFilename, layout, name_data)
        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="NameTagType not supported")

    response = FilePath(filename=outputFilename)

    await wsConnectionManager.sendToPrinter(printerCode, response.json())

    return response


@router.get('/{printer_code}', response_model=List[FilePath])
def get_name_tags(printer_code: PrinterCode):
    return getFilesInPrinterQueue(printer_code)

@router.delete('/{printer_code}', response_model=List[FilePath])
def get_name_tags(printer_code: PrinterCode):
    return deleteFilesInPrinterQueue(printer_code)


@router.get('/{printer_code}/{filename}',
            response_class=FileResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_name_tag(printer_code : PrinterCode, filename : str):
    securedFileName = secure_filename(filename)
    nameTagFilename = nameTagsPath + printer_code + \
        '/' + os.path.basename(securedFileName)
        
    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        return FileResponse(path=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name tag not found")


@router.delete('/{printer_code}/{filename}', 
            response_model=FilePath,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def delete_name_tag(printer_code: PrinterCode, filename: str):
    securedFileName = secure_filename(filename)
    nameTagFilename = nameTagsPath + printer_code + \
        '/' + os.path.basename(securedFileName)

    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        os.remove(nameTagFilename)
        return FilePath(filename=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="NameTag not found")