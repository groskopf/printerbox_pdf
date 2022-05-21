from datetime import date as date
from calendar import calendar
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import List
from booking.booking import Booking
from booking.booking_calendar import BookingCalendar
from booking.printer_code import PrinterCode

from endpoint.name_data import NameData
from endpoint.images import postImage
from endpoint.name_tag import postNameTag
from endpoint.name_tag_sheet import postNameTagSheet
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf.name_tag_sheet_type import NameTagSheetType

app = FastAPI()

calendar = BookingCalendar()
calendar.load()


app.mount('/images', StaticFiles(directory="./images"), name="images")
app.mount('/printer_queue', StaticFiles(directory="./printer_queue"),
          name="printer_queue")


@app.post('/image_upload')
def postImageUpload(file: UploadFile = File(...)):
    return postImage(file)


@app.post('/name_tag/{name_tag_type}/{layout}')
def nameTag(printer_code: str, nameTagType: NameTagType, layout: Layout, nameData: NameData):
    return postNameTag(nameTagType, layout, nameData)


@app.post('/name_tag_sheet/{name_tag_sheet_type}/{layout}')
def nameTagSheet(nameTagSheetType: NameTagSheetType, layout: Layout, nameDataList: List[NameData]):
    return postNameTagSheet(nameTagSheetType, layout, nameDataList)


@app.post('/booking/add')
def nameTagSheet(startDate: date, endDate: date, printerCode: PrinterCode):
    booking = calendar.add(startDate, endDate, printerCode)
    calendar.save()
    return booking


@app.post('/booking/delete')
def nameTagSheet(bookingCode: str):
    booking = calendar.delete(bookingCode)
    calendar.save()
    return booking


@app.get('/booking/')
def nameTagSheet(startDate: str = None, endDate: str = None):
    return calendar.bookings


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
