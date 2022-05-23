import os
import base64
import uuid
from typing import List

from filePaths import bookingsPath
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from datetime import date as date
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode

defaultBookingFile = bookingsPath + 'bookings.json'
class Booking(BaseModel):
    startDate: date
    endDate: date
    printerCode: PrinterCode
    code: str
    nameTagType: NameTagType

class Bookings(BaseModel):
    list: List[Booking] = []

class Calendar(BaseModel):
    bookings: Bookings = Bookings()

    def save(self, filename: str = defaultBookingFile):
        with open(filename, 'w') as file:
            file.write(self.bookings.json())

    def load(self, filename: str = defaultBookingFile):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                rawJson: str = file.read()
                if rawJson:
                    self.bookings = Bookings.parse_raw(rawJson)

    def isOverlappingExitingBooking(self, newBooking: Booking):
        for existingBooking in self.bookings.list:
            if existingBooking.printerCode == newBooking.printerCode:
                if (newBooking.startDate <= existingBooking.endDate) and (existingBooking.startDate <= newBooking.endDate):
                    return True
        return False

    def getBooking(self, bookingCode: str):
        for booking in self.bookings.list:
            if booking.code == bookingCode:
                return booking
        return None


calendar = Calendar()
calendar.load()

router = APIRouter()


@router.get('/', response_model=List[Booking])
def getNameTagSheet():
    return calendar.bookings


@router.post('/', response_model=Booking, status_code=status.HTTP_201_CREATED)
def postNameTagSheet(startDate: date, endDate: date, printerCode: PrinterCode, nameTagType : NameTagType):
    if startDate > endDate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dates are in wrong order")

    booking = Booking(startDate=startDate,
                      endDate=endDate,
                      printerCode=printerCode,
                      code=base64.urlsafe_b64encode(uuid.uuid4().bytes)[0:15].upper(),
                      nameTagType=nameTagType)
    if(not calendar.isOverlappingExitingBooking(booking)):
        calendar.bookings.list.append(booking)
        calendar.save()
        return booking
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Printer has booking in same period")


@router.put('/{bookingCode}', response_model=Booking)
def putNameTagSheet(bookingCode: str, startDate: date, endDate: date, printerCode: PrinterCode, nameTagType : NameTagType):
    for i in range(len(calendar.bookings.list)):
        if calendar.bookings.list[i].code == bookingCode:
            booking = Booking(startDate=startDate, endDate=endDate, printerCode=printerCode, code=bookingCode, nameTagType=nameTagType)
            calendar.bookings.list[i] = booking
            calendar.save()
            return booking
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.delete('/{bookingCode}', response_model=Booking)
def deleteNameTagSheet(bookingCode: str):
    for i in range(len(calendar.bookings.list)):
        if calendar.bookings.list[i].code == bookingCode:
            booking = calendar.bookings.list[i]
            del calendar.bookings.list[i]
            return booking
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
