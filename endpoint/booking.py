from datetime import date as date
from printer_code import PrinterCode
from pdf.name_tag_type import NameTagType

from pydantic import BaseModel

class Booking(BaseModel):
    start_date: date = None
    end_date: date = None
    printer_code: PrinterCode = None
    booking_code: str = None
    name_tag_type: NameTagType = None
    