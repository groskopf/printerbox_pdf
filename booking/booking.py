from pydantic import BaseModel
from datetime import date as date
from booking.printer_code import PrinterCode

class Booking(BaseModel):
    startDate : date
    endDate : date
    printerCode : PrinterCode
    code : str = ""

    def __init__(self, startDate : date, endDate : date, printerCode : PrinterCode, code : str):
        super().__init__(startDate=startDate, endDate=endDate, printerCode=printerCode, code=code)
    