import os
import base64
import uuid
from typing import List

from pydantic import BaseModel
from fastapi import HTTPException
from datetime import date as date
from booking.booking import Booking
from booking.printer_code import PrinterCode


class BookingList(BaseModel):
    bookings: List[Booking] = []


class BookingCalendar():

    calendar: BookingList

    def __init__(self):
        self.calendar = BookingList()

    def add(self, startDate: date, endDate: date, printerCode: PrinterCode):
        # TODO check if it collides with other bookings
        booking = Booking(startDate, endDate, printerCode,
                          base64.b64encode(uuid.uuid4().bytes))
        if(not self.isOverlappingExitingBooking(booking)):
            self.calendar.bookings.append(booking)
            return booking
        raise HTTPException(status_code=404, detail="Item not found")

    def update(self, bookingCode : str, startDate: date, endDate: date, printerCode: PrinterCode):
        for i in range(len(self.calendar.bookings)):
            if self.calendar.bookings[i].code == bookingCode:
                booking = Booking(startDate, endDate, printerCode, bookingCode)
                self.calendar.bookings[i] = booking
                return booking
        raise HTTPException(status_code=404, detail="Item not found")

    def delete(self, bookingCode: str):
        for i in range(len(self.calendar.bookings)):
            if self.calendar.bookings[i].code == bookingCode:
                booking = self.calendar.bookings[i]
                del self.calendar.bookings[i]
                return booking
        raise HTTPException(status_code=404, detail="Item not found")

    def save(self, filename: str = 'bookings.json'):
        with open(filename, 'w') as file:
            file.write(self.calendar.json())

    def load(self, filename: str = 'bookings.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                rawJson: str = file.read()
                if rawJson:
                    self.calendar = BookingList.parse_raw(rawJson)

    def isOverlappingExitingBooking(self, newBooking: Booking):
        for existingBooking in self.calendar.bookings:
            if existingBooking.printerCode == newBooking.printerCode:
                if (newBooking.startDate <= existingBooking.endDate) and (existingBooking.startDate <= newBooking.endDate):
                    return True
        return False

    def getBooking(self, bookingCode: str):
        for booking in self.calendar.bookings:
            if booking.code == bookingCode:
                return booking
        return None
