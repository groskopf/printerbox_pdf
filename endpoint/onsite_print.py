import os
from uuid import uuid4
from datetime import date as date
from fastapi import APIRouter, HTTPException, status
from werkzeug.utils import secure_filename

from filePaths import imagesPath, queuesPath
from printer_code import PrinterCode
from endpoint.bookings import calendar
from endpoint.bookings import Booking
from endpoint.printerbox import Filename, wsConnectionManager
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf import name_tag_4786103

router = APIRouter()

def checkImageFileExist(nameData: NameData):
    imageName = imagesPath + nameData.imageName
    if imageName:
        if not os.path.exists(imageName) or not os.path.isfile(imageName):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

def findBooking(bookingCode):
    booking : Booking = calendar.getBooking(bookingCode)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.startDate > date.today() or date.today() > booking.endDate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking not valid today")
    return booking.printerCode, booking.nameTagType



@router.post('/{layout}', status_code=status.HTTP_201_CREATED)
async def nameTag(bookingCode: str, layout: Layout, nameData: NameData):
    nameData.imageName = secure_filename(nameData.imageName)
    checkImageFileExist(nameData)
    
    printerCode, nameTagType = findBooking(bookingCode)

    outputPath = queuesPath + printerCode + '/'
    outputFilename =  outputPath+ nameTagType + '_' + uuid4().hex + '.pdf'

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    match nameTagType:
        case NameTagType._4786103:
            name_tag_4786103.create(outputFilename, layout, nameData)
        case _:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NameTagType not supported")

    response = Filename(filename=outputFilename)

    await wsConnectionManager.sendToPrinter(printerCode, response.json())
    
    return response
