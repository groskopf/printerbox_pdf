from fastapi import status
from fastapi.testclient import TestClient
from datetime import date as date

import pytest

from main import app
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode
from endpoint.booking_calendar import calendar

client = TestClient(app)


@pytest.fixture
def deleteBookings():
    # Get all bookings
    response = client.get('/bookings', headers={'access_token': '123admin'})
    assert response.status_code == 200

    # Delete all bookings
    bookings = response.json()
    for booking in bookings:
        response = client.delete(
            '/bookings/' + booking['booking_code'], headers={'access_token': '123admin'})
        assert response.status_code == 200

    calendar.load()


def newBooking(startDate: date, endDate: date, printerCode: PrinterCode, nameTagType: NameTagType):

    # Create a new booking
    response = client.post('/bookings/?start_date=' + startDate.isoformat() +
                           '&end_date=' + endDate.isoformat() +
                           '&printer_code=' + printerCode +
                           '&name_tag_type=' + nameTagType,
                           headers={'access_token': '123admin'})
    assert response.status_code == 201

    booking = response.json()
    assert booking['start_date'] == startDate.isoformat()
    assert booking['end_date'] == endDate.isoformat()
    assert booking['printer_code'] == printerCode
    assert booking['name_tag_type'] == nameTagType
    bookingCode = booking['booking_code']
    assert bookingCode
    return bookingCode


def getBookings():
    response = client.get('/bookings', headers={'access_token': '123admin'})
    assert response.status_code == 200
    bookings = response.json()
    return bookings


def test_clean_booking_list(deleteBookings):
    response = client.get("/bookings", headers={'access_token': '123admin'})
    assert response.status_code == 200
    bookings = response.json()
    assert bookings == []


def test_add_booking(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1974-08-22'),
                             date.fromisoformat('1974-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    bookings = getBookings()
    assert len(bookings) == 1

    # Test that we have the date we need
    booking = bookings[0]
    assert booking['start_date'] == '1974-08-22'
    assert booking['end_date'] == '1974-09-22'
    assert booking['printer_code'] == '1OPYKBGXVN_1'
    assert booking['booking_code'] == bookingCode
    assert booking['name_tag_type'] == NameTagType._4786103

    # Create another booking
    bookingCode = newBooking(date.fromisoformat('1984-08-22'),
                             date.fromisoformat('1984-09-26'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    # Test that we got the new booking
    bookings = getBookings()
    assert len(bookings) == 2

    # Fail creating an overlapping booking
    response = client.post(
        'bookings/?start_date=1984-08-21&end_date=1984-08-22&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': '123admin'})
    assert response.status_code == 409

    # Fail creating an overlapping booking
    response = client.post(
        'bookings/?start_date=1984-08-26&end_date=1984-08-29&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': '123admin'})
    assert response.status_code == 409

    # Fail creating an overlapping booking
    response = client.post(
        'bookings/?start_date=1984-08-23&end_date=1984-08-25&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': '123admin'})
    assert response.status_code == 409

    # Fail creating mixed around date order
    response = client.post(
        'bookings/?start_date=1984-08-29&end_date=1984-08-25&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': '123admin'})
    assert response.status_code == 400


def test_get_booking(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1974-08-22'),
                             date.fromisoformat('1974-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    response = client.get('/bookings/' + bookingCode,
                          headers={'access_token': '123admin'})
    assert response.status_code == 200

    booking = response.json()
    assert booking['start_date'] == '1974-08-22'
    assert booking['end_date'] == '1974-09-22'
    assert booking['printer_code'] == '1OPYKBGXVN_1'
    assert booking['name_tag_type'] == NameTagType._4786103
    assert bookingCode == booking['booking_code']


def test_get_booking_printer(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1974-08-22'),
                             date.fromisoformat('1974-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4760100)
    bookingCode = newBooking(date.today(),
                             date.today(),
                             PrinterCode._21YG0T6L8O_5,
                             NameTagType._4786103)

    response = client.get('/bookings/printer/' + PrinterCode._21YG0T6L8O_5,
                          headers={'access_token': '123admin'})
    assert response.status_code == 200

    booking = response.json()
    assert date.fromisoformat(booking['start_date']) == date.today()
    assert date.fromisoformat(booking['end_date']) == date.today()
    assert booking['printer_code'] == '21YG0T6L8O_5'
    assert booking['name_tag_type'] == NameTagType._4786103
    assert bookingCode == booking['booking_code']


def test_update_booking(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1984-08-22'),
                             date.fromisoformat('1984-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    # Update booking
    response = client.put('bookings/' + bookingCode +
                          '?start_date=1984-08-22' +
                          '&end_date=1984-09-22' +
                          '&printer_code=1OPYKBGXVN_1' +
                          '&name_tag_type=' + NameTagType._4786103, headers={'access_token': '123admin'})
    assert response.status_code == 200

    booking = response.json()
    assert booking['start_date'] == '1984-08-22'
    assert booking['end_date'] == '1984-09-22'
    assert booking['printer_code'] == '1OPYKBGXVN_1'
    bookingCode = booking['booking_code']
    assert booking['name_tag_type'] == NameTagType._4786103

    # Test that we got the new booking
    bookings = getBookings()
    assert len(bookings) == 1

    # Test that we have the date we need
    booking = bookings[0]
    assert booking['start_date'] == '1984-08-22'
    assert booking['end_date'] == '1984-09-22'
    assert booking['printer_code'] == '1OPYKBGXVN_1'
    assert booking['booking_code'] == bookingCode
    assert booking['name_tag_type'] == NameTagType._4786103

    # Fail update non existing booking
    response = client.put('bookings/' + 'FAKE_CODE' +
                          '?start_date=1984-08-22' +
                          '&end_date=1984-09-22' +
                          '&printer_code=1OPYKBGXVN_1' +
                          '&name_tag_type=' + NameTagType._4786103,
                          headers={'access_token': '123admin'})
    assert response.status_code == 404


def test_delete_booking(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1984-08-22'),
                             date.fromisoformat('1984-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4760100)

    # Test we don't have any bookings
    assert len(getBookings()) == 1

    # Fail delete non existing booking
    response = client.delete('bookings/' + 'FAKE_CODE',
                             headers={'access_token': '123admin'})
    assert response.status_code == 404

    # Delete booking
    response = client.delete('bookings/' + bookingCode,
                             headers={'access_token': '123admin'})
    assert response.status_code == 200

    # Test we don't have any bookings
    assert len(getBookings()) == 0


def test_get_bookings_access_rights(deleteBookings):
    response = client.get('/bookings')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/bookings', headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/bookings', headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/bookings',
                          headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_bookings_access_rights(deleteBookings):
    response = client.post(
        'bookings/?start_date=2984-08-21&end_date=2984-08-22&printer_code=1OPYKBGXVN_1&name_tag_type=4786103')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post(
        'bookings/?start_date=2984-08-21&end_date=2984-08-22&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post(
        'bookings/?start_date=2984-08-21&end_date=2984-08-22&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post(
        'bookings/?start_date=2984-08-21&end_date=2984-08-22&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(
        'bookings/?start_date=2994-08-21&end_date=2994-08-22&printer_code=1OPYKBGXVN_1&name_tag_type=4786103',
        headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_201_CREATED


def test_get_booking_access_rights(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1964-08-22'),
                             date.fromisoformat('1964-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4760100)

    response = client.get('/bookings/' + bookingCode)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/bookings/' + bookingCode,
                          headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/bookings/' + bookingCode,
                          headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/bookings/' + bookingCode,
                          headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK

    bookingCode = newBooking(date.fromisoformat('1974-08-22'),
                             date.fromisoformat('1974-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4760100)

    response = client.get('/bookings/' + bookingCode,
                          headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK


def test_put_booking_access_rights(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1987-08-22'),
                             date.fromisoformat('1987-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    response = client.put('bookings/' + bookingCode +
                          '?start_date=1987-08-22' +
                          '&end_date=1987-09-22' +
                          '&printer_code=1OPYKBGXVN_1' +
                          '&name_tag_type=' + NameTagType._4786103,
                          headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.put('bookings/' + bookingCode +
                          '?start_date=1987-08-22' +
                          '&end_date=1987-09-22' +
                          '&printer_code=1OPYKBGXVN_1' +
                          '&name_tag_type=' + NameTagType._4786103,
                          headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.put('bookings/' + bookingCode +
                          '?start_date=1987-08-22' +
                          '&end_date=1987-09-22' +
                          '&printer_code=1OPYKBGXVN_1' +
                          '&name_tag_type=' + NameTagType._4786103,
                          headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_200_OK
    response = client.put('bookings/' + bookingCode +
                          '?start_date=1987-08-22' +
                          '&end_date=1987-09-22' +
                          '&printer_code=1OPYKBGXVN_1' +
                          '&name_tag_type=' + NameTagType._4786103,
                          headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK


def test_delete_booking_access_rights(deleteBookings):
    bookingCode = newBooking(date.fromisoformat('1987-08-22'),
                             date.fromisoformat('1987-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    response = client.delete('bookings/' + bookingCode,
                             headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.delete('bookings/' + bookingCode,
                             headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.delete('bookings/' + bookingCode,
                             headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_200_OK

    bookingCode = newBooking(date.fromisoformat('1987-08-22'),
                             date.fromisoformat('1987-09-22'),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    response = client.delete('bookings/' + bookingCode,
                             headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK


def test_get_booking_printer_access_rights(deleteBookings):
    bookingCode = newBooking(date.today(),
                             date.today(),
                             PrinterCode._21YG0T6L8O_5,
                             NameTagType._4786103)

    response = client.get('/bookings/printer/' + PrinterCode._21YG0T6L8O_5,
                          headers={'access_token': 'printer_4'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.get('/bookings/printer/' + PrinterCode._21YG0T6L8O_5,
                          headers={'access_token': 'printer_5'})
    assert response.status_code == 200

    booking = response.json()
    assert date.fromisoformat(booking['start_date']) == date.today()
    assert date.fromisoformat(booking['end_date']) == date.today()
    assert booking['printer_code'] == '21YG0T6L8O_5'
    assert booking['name_tag_type'] == NameTagType._4786103
    assert bookingCode == booking['booking_code']
