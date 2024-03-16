from datetime import date
import os
from typing import List
from pydantic import RootModel, TypeAdapter

from endpoint.booking import Booking
from printer_code import PrinterCode
from site_paths import bookingsPath

defaultBookingFile = bookingsPath + 'bookings.json'


class BookingCalendar(RootModel):

    root: List[Booking] = []

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item : int) -> Booking:
        return self.root[item]
    
    def __setitem__(self, item : int, booking : Booking):
        self.root[item] = booking
    
    def __len__(self):
        return len(self.root)
    
    def append(self, booking : Booking):
        self.root.append(booking)
   
    def pop(self, index : int):
        if 0 <= index < len(self.root):
            self.root.pop(index)
        else:
            raise IndexError("Index out of range")
        
    def save(self, filename: str = defaultBookingFile):
        with open(filename, 'w') as file:
            file.write(self.model_dump_json())

    def load(self, filename: str = defaultBookingFile):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                rawJson: str = file.read()
                if rawJson:
                    self.root = TypeAdapter(BookingCalendar).validate_json(rawJson)

    def isOverlappingExitingBooking(self, newBooking: Booking):
        for existingBooking in self.root:
            if existingBooking.printer_code == newBooking.printer_code:
                if (newBooking.start_date <= existingBooking.end_date) and (existingBooking.start_date <= newBooking.end_date):
                    return True
        return False

    def getBooking(self, bookingCode: str):
        for booking in self.root:
            if booking.booking_code == bookingCode:
                return booking
        return None

    def getPrinterBooking(self, printer_code: PrinterCode):
        today = date.today()
        for booking in self.root:
            if booking.printer_code == printer_code:
                if booking.start_date <= today and today <= booking.end_date:
                    print(f"Booking: {booking}")
                    return booking
        return None


calendar : BookingCalendar = BookingCalendar()
calendar.load()