import json
import os
import base64
import uuid
from typing import List

from filePaths import bookingsPath
from pydantic import BaseModel, parse_raw_as
from pydantic.json import pydantic_encoder
from fastapi import APIRouter, HTTPException, status
from datetime import date as date
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode

defaultBookingFile = bookingsPath + 'bookings.json'
class Booking(BaseModel):
    start_date: date
    end_date: date
    printer_code: PrinterCode
    code: str
    name_tag_type: NameTagType

class Calendar(BaseModel):
    bookings: List[Booking] = []

    def save(self, filename: str = defaultBookingFile):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.bookings, default=pydantic_encoder))

    def load(self, filename: str = defaultBookingFile):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                rawJson: str = file.read()
                if rawJson:
                    self.bookings = parse_raw_as(List[Booking], rawJson)

    def isOverlappingExitingBooking(self, newBooking: Booking):
        for existingBooking in self.bookings:
            if existingBooking.printer_code == newBooking.printer_code:
                if (newBooking.start_date <= existingBooking.end_date) and (existingBooking.start_date <= newBooking.end_date):
                    return True
        return False

    def getBooking(self, bookingCode: str):
        for booking in self.bookings:
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
def postNameTagSheet(start_date: date, end_date: date, printer_code: PrinterCode, name_tag_type : NameTagType):
    if start_date > end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dates are in wrong order")

    booking = Booking(start_date=start_date,
                      end_date=end_date,
                      printer_code=printer_code,
                      code=base64.urlsafe_b64encode(uuid.uuid4().bytes)[0:15].upper(),
                      name_tag_type=name_tag_type)
    if(not calendar.isOverlappingExitingBooking(booking)):
        calendar.bookings.append(booking)
        calendar.save()
        return booking
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Printer has booking in same period")


@router.put('/{booking_code}', response_model=Booking)
def putNameTagSheet(booking_code: str, start_date: date, end_date: date, printer_code: PrinterCode, name_tag_type : NameTagType):
    for i in range(len(calendar.bookings)):
        if calendar.bookings[i].code == booking_code:
            booking = Booking(start_date=start_date, end_date=end_date, printer_code=printer_code, code=booking_code, name_tag_type=name_tag_type)
            calendar.bookings[i] = booking
            calendar.save()
            return booking
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.delete('/{booking_code}', response_model=Booking)
def deleteNameTagSheet(booking_code: str):
    for i in range(len(calendar.bookings)):
        if calendar.bookings[i].code == booking_code:
            booking = calendar.bookings[i]
            del calendar.bookings[i]
            return booking
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
