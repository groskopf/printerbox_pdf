import os
from uuid import uuid4
from datetime import date as date
from fastapi import APIRouter, HTTPException, status

from endpoint.bookings import calendar
from endpoint.bookings import Booking
from name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf import name_tag_4786103
from printer_code import PrinterCode

router = APIRouter()

def checkImageFileExist(nameData: NameData):
    imageName = './images/' + nameData.imageName
    if imageName:
        if not os.path.exists(imageName) or not os.path.isfile(imageName):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

def findPrinterFromBooking(bookingCode):
    booking : Booking = calendar.getBooking(bookingCode)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if booking.startDate > date.today() or date.today() > booking.endDate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking not valid today")
    return booking.printerCode 



@router.post('/{nameTagType}/{layout}', status_code=status.HTTP_201_CREATED)
def nameTag(bookingCode: str, nameTagType: NameTagType, layout: Layout, nameData: NameData):

    checkImageFileExist(nameData)
    
    printerCode : PrinterCode = findPrinterFromBooking(bookingCode)

    outputPath = 'queues/' + printerCode + '/'
    outputFilename =  outputPath+ nameTagType + '_' + uuid4().hex + '.pdf'

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    match nameTagType:
        case NameTagType._4786103:
            name_tag_4786103.create(outputFilename, layout, nameData)
        case _:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NameTagType not supported")

    return {"filename": outputFilename}
