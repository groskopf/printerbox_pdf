import base64
from datetime import date
import uuid
from typing import List


from details import Details
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode
from fastapi import APIRouter, HTTPException, status, Security
from fastapi.security.api_key import APIKey

from endpoint.booking import Booking
from endpoint.booking_calendar import BookingCalendar, calendar
from endpoint.name_tags_ws import WSConnectionManager
from endpoint.authentication import AccessScope, authenticate_api_key, authenticate_printer_api_key

router = APIRouter()


@router.get('/', response_model=BookingCalendar)
def get_bookings(api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER_BOOKING])):
    return calendar


@router.get('/printer/{printer_code}', response_model=Booking)
def get_bookings(printer_code : str, api_key: APIKey = Security(authenticate_printer_api_key, scopes=[AccessScope._PRINTER])):
    bookingCode = calendar.getPrinterBooking(printer_code)
    if bookingCode:
        return bookingCode

    raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No current bookings")


@router.post('/',
             response_model=Booking,
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": Details},
                 status.HTTP_409_CONFLICT: {"model": Details}
             })
async def new_booking(start_date: date, end_date: date, printer_code: PrinterCode, name_tag_type: NameTagType,
                api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER_BOOKING])):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Dates are in wrong order")

    booking = Booking(start_date=start_date,
                      end_date=end_date,
                      printer_code=printer_code,
                      booking_code=base64.b32encode(uuid.uuid4().bytes)[
                          0:15].upper(),
                      name_tag_type=name_tag_type)

    if (calendar.isOverlappingExitingBooking(booking)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Printer has booking in same period")

    calendar.append(booking)
    calendar.save()
    return booking


@router.get('/{booking_code}',
            response_model=Booking,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_booking(booking_code: str,
                api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER_BOOKING, AccessScope._CONFERENCE])):
    for i in range(len(calendar)):
        if calendar[i].booking_code == booking_code:
            return calendar[i]

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")


@router.put('/{booking_code}',
            response_model=Booking,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def update_booking(booking_code: str, start_date: date, end_date: date, printer_code: PrinterCode, name_tag_type: NameTagType,
                   api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER_BOOKING])):
    for i in range(len(calendar)):
        if calendar[i].booking_code == booking_code:
            booking = Booking(start_date=start_date,
                              end_date=end_date,
                              printer_code=printer_code,
                              booking_code=booking_code,
                              name_tag_type=name_tag_type)
            calendar[i] = booking
            calendar.save()
            return booking

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")


@router.delete('/{booking_code}',
               response_model=Booking,
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": Details},
               })
def delete_booking(booking_code: str,
                   api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER_BOOKING])):
    for i in range(len(calendar)):
        if calendar[i].booking_code == booking_code:
            booking = calendar[i]
            calendar.pop(i)
            calendar.save()
            return booking

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")
