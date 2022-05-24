import os
from uuid import uuid4
from datetime import date as date
from fastapi import APIRouter, HTTPException, status
from werkzeug.utils import secure_filename

from details import Details
from site_paths import imagesPath, queuesPath
from printer_code import PrinterCode
from endpoint.bookings import calendar
from endpoint.bookings import Booking
from endpoint.printerbox import wsConnectionManager
from file_path import FilePath
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf import name_tag_4786103

router = APIRouter()


def checkImageFileExist(nameData: NameData):
    imageName = imagesPath + nameData.imageName
    if imageName:
        if not os.path.exists(imageName) or not os.path.isfile(imageName):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


def findBooking(bookingCode):
    booking: Booking = calendar.getBooking(bookingCode)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.start_date > date.today() or date.today() > booking.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Booking not valid today")
    return booking.printer_code, booking.name_tag_type


@router.post('/{layout}',
             response_model=FilePath,
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": Details},
                 status.HTTP_404_NOT_FOUND: {"model": Details}
             })
async def nameTag(booking_code: str, layout: Layout, name_data: NameData):
    name_data.imageName = secure_filename(name_data.imageName)
    checkImageFileExist(name_data)

    printerCode, nameTagType = findBooking(booking_code)

    outputPath = queuesPath + printerCode + '/'
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
