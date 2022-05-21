import os
import base64
import uuid
from typing import List

from pydantic import BaseModel
from datetime import date as date
from booking.booking import Booking
from booking.printer_code import PrinterCode


class BookingList(BaseModel):
    list: List[Booking] = []


class BookingCalendar():

    bookings: BookingList

    def __init__(self):
        self.bookings = BookingList()

    def save(self, filename: str = 'bookings.json'):
        with open(filename, 'w') as file:
            file.write(self.bookings.json())

    def load(self, filename: str = 'bookings.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                rawJson: str = file.read()
                if rawJson:
                    self.bookings = BookingList.parse_raw(rawJson)

    def add(self, startDate: date, endDate: date, printerCode: PrinterCode):
        # TODO check if it collides with other bookings
        booking = Booking(startDate, endDate, printerCode,
                          base64.b64encode(uuid.uuid4().bytes))
        self.bookings.list.append(booking)
        return booking

    def getBooking(self, bookingCode: str):
        for booking in self.bookings.list:
            if booking.code == bookingCode:
                return booking
        return None

    def delete(self, bookingCode: str):

        booking = self.getBooking(bookingCode)
        if booking:
            self.bookings.list.remove(booking)
        return booking
        # self.booking = [        booking for booking in self.bookings.list if not booking == bookingCode]
