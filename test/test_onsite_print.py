import os
from datetime import date as date, timedelta
from fastapi.testclient import TestClient
import pytest

from main import app
from printer_code import PrinterCode
from test.test_bookings import createBooking, clearBookingList
from test.test_upload import uploadImage

client = TestClient(app)

@pytest.fixture
def removeOldPrints():
    for root, dirs, files in os.walk('./queues', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def createNameTag(bookingCode: str):
    uploadImage('./test/images/logo.jpg')
    body = {"name": "string",
            "description1": "string",
            "description2": "string",
            "description3": "string",
            "description4": "string",
            "imageName": "logo.jpg"}
    response = client.post('/onsite_print/4786103/layout_1?bookingCode=' + bookingCode,
                           json=body)
    return response


def test_new_name_tag(clearBookingList, removeOldPrints):
    # Today
    bookingCode = createBooking(date.today(),
                                date.today(),
                                PrinterCode._XDESP95271_p)

    # Create a name tag
    response = createNameTag(bookingCode)
    assert response.status_code == 201

    # Do file exist locally
    filename = response.json()['filename']
    assert os.path.exists(filename) and os.path.isfile(filename)

    # TODO can we download it? 


def test_booking_wrong_dates(clearBookingList, removeOldPrints):
    # Too early
    bookingCode = createBooking(date.today()+timedelta(days=1),
                                date.today()+timedelta(days=1),
                                PrinterCode._XDESP95271_p)

    # Create a name tag
    response = createNameTag(bookingCode)
    assert response.status_code == 400
    assert not response
    
    # Too late
    bookingCode = createBooking(date.today()-timedelta(days=1),
                                date.today()-timedelta(days=1),
                                PrinterCode._XDESP95271_p)

    # Create a name tag
    response = createNameTag(bookingCode)
    assert response.status_code == 400
    assert not response


def test_bad_booking(clearBookingList, removeOldPrints):
    bookingCode = 'FAKE_BOOKING'

    # Create a name tag
    response = createNameTag(bookingCode)
    assert response.status_code == 404
    assert not response

