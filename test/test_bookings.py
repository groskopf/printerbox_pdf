from fastapi.testclient import TestClient
from datetime import date as date

import pytest

from main import app
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode
from endpoint.bookings import calendar

client = TestClient(app)


@pytest.fixture
def clearBookingList():
    # Get all bookings
    response = client.get('/bookings')
    assert response.status_code == 200

    # Delete all bookings
    bookings = response.json()
    for booking in bookings:
        response = client.delete('/bookings/' + booking['code'])
        assert response.status_code == 200

    calendar.save()


def createBooking(startDate: date, endDate: date, printerCode: PrinterCode, nameTagType: NameTagType):

    # Create a new booking
    response = client.post('/bookings/?startDate=' + startDate.isoformat() +
                           '&endDate=' + endDate.isoformat() +
                           '&printerCode=' + printerCode +
                           '&nameTagType=' + nameTagType)
    assert response.status_code == 201

    booking = response.json()
    assert booking['startDate'] == startDate.isoformat()
    assert booking['endDate'] == endDate.isoformat()
    assert booking['printerCode'] == printerCode
    assert booking['nameTagType'] == nameTagType
    bookingCode = booking['code']
    assert bookingCode
    return bookingCode


def getBookingList():
    response = client.get('/bookings')
    assert response.status_code == 200
    bookings = response.json()
    return bookings


def test_clean_booking_list(clearBookingList):
    response = client.get("/bookings")
    assert response.status_code == 200
    bookings = response.json()
    assert bookings == []


def test_add_booking(clearBookingList):
    bookingCode = createBooking(date.fromisoformat('1974-08-22'),
                                date.fromisoformat('1974-09-22'),
                                PrinterCode._XDESP95271_p,
                                NameTagType._4786103)

    bookings = getBookingList()
    assert len(bookings) == 1

    # Test that we have the date we need
    booking = bookings[0]
    assert booking['startDate'] == '1974-08-22'
    assert booking['endDate'] == '1974-09-22'
    assert booking['printerCode'] == 'XDESP95271_p'
    assert booking['code'] == bookingCode
    assert booking['nameTagType'] == NameTagType._4786103

    # Create another booking
    bookingCode = createBooking(date.fromisoformat('1984-08-22'),
                                date.fromisoformat('1984-09-26'),
                                PrinterCode._XDESP95271_p,
                                NameTagType._4786103)

    # Test that we got the new booking
    bookings = getBookingList()
    assert len(bookings) == 2

    # Fail creating an overlapping booking
    response = client.post(
        'bookings/?startDate=1984-08-21&endDate=1984-08-22&printerCode=XDESP95271_p&nameTagType=4786103')
    assert response.status_code == 409

    # Fail creating an overlapping booking
    response = client.post(
        'bookings/?startDate=1984-08-26&endDate=1984-08-29&printerCode=XDESP95271_p&nameTagType=4786103')
    assert response.status_code == 409

    # Fail creating an overlapping booking
    response = client.post(
        'bookings/?startDate=1984-08-23&endDate=1984-08-25&printerCode=XDESP95271_p&nameTagType=4786103')
    assert response.status_code == 409

    # Fail creating mixed around date order
    response = client.post(
        'bookings/?startDate=1984-08-29&endDate=1984-08-25&printerCode=XDESP95271_p&nameTagType=4786103')
    assert response.status_code == 400


def test_update_booking(clearBookingList):
    bookingCode = createBooking(date.fromisoformat('1984-08-22'),
                                date.fromisoformat('1984-09-22'),
                                PrinterCode._XDESP95271_p,
                                NameTagType._4786103)

    # Update booking
    response = client.put('bookings/' + bookingCode +
                          '?startDate=1984-08-22' +
                          '&endDate=1984-09-22' +
                          '&printerCode=XDESP95271_p' +
                          '&nameTagType=' + NameTagType._4786103)
    assert response.status_code == 200

    booking = response.json()
    assert booking['startDate'] == '1984-08-22'
    assert booking['endDate'] == '1984-09-22'
    assert booking['printerCode'] == 'XDESP95271_p'
    bookingCode = booking['code']
    assert booking['nameTagType'] == NameTagType._4786103

    # Test that we got the new booking
    bookings = getBookingList()
    assert len(bookings) == 1

    # Test that we have the date we need
    booking = bookings[0]
    assert booking['startDate'] == '1984-08-22'
    assert booking['endDate'] == '1984-09-22'
    assert booking['printerCode'] == 'XDESP95271_p'
    assert booking['code'] == bookingCode
    assert booking['nameTagType'] == NameTagType._4786103

    # Fail update non existing booking
    response = client.put('bookings/' + 'FAKE_CODE' +
                          '?startDate=1984-08-22' +
                          '&endDate=1984-09-22' +
                          '&printerCode=XDESP95271_p' +
                          '&nameTagType=' + NameTagType._4786103)
    assert response.status_code == 404


def test_delete_booking(clearBookingList):
    bookingCode = createBooking(date.fromisoformat('1984-08-22'),
                                date.fromisoformat('1984-09-22'),
                                PrinterCode._XDESP95271_p,
                                NameTagType._47150106)

    # Test we don't have any bookings
    assert len(getBookingList()) == 1

    # Fail delete non existing booking
    response = client.delete('bookings/' + 'FAKE_CODE')
    assert response.status_code == 404

    # Delete booking
    response = client.delete('bookings/' + bookingCode)
    assert response.status_code == 200

    # Test we don't have any bookings
    assert len(getBookingList()) == 0
