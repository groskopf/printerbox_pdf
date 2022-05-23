import os
from datetime import date as date, timedelta
from fastapi.testclient import TestClient
import pytest

from main import app
from site_paths import queuesPath
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode
from test.test_bookings import createBooking, clearBookingList
from test.test_upload import uploadImage

client = TestClient(app)


def deleteAllFilesInQueues():
    for root, dirs, files in os.walk(queuesPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


@pytest.fixture
def removeOldPrints():
    deleteAllFilesInQueues()


def createNameTag(bookingCode: str):
    image = os.path.basename(uploadImage('./test/images/logo.jpg'))
    body = {"name": "string",
            "description1": "string",
            "description2": "string",
            "description3": "string",
            "description4": "string",
            "imageName": image}
    response = client.post('/onsite_print/layout_1?booking_code=' + bookingCode, json=body)
    return response


def newNameTag(bookingCode: str):
    response = createNameTag(bookingCode)
    assert response.status_code == 201
    filename = response.json()['filename']
    assert filename
    return filename


def test_new_name_tag(clearBookingList, removeOldPrints):
    # Today
    bookingCode = createBooking(date.today(),
                                date.today(),
                                PrinterCode._XDESP95271_p,
                                NameTagType._4786103)

    # Create a name tag
    filename = newNameTag(bookingCode)

    # Do file exist locally
    assert os.path.exists(filename) and os.path.isfile(filename)

    # TODO can we download it?


def test_booking_wrong_dates(clearBookingList, removeOldPrints):
    # Too early
    bookingCode = createBooking(date.today()+timedelta(days=1),
                                date.today()+timedelta(days=1),
                                PrinterCode._XDESP95271_p,
                                NameTagType._4786103)

    # Create a name tag
    response = createNameTag(bookingCode)
    assert response.status_code == 400
    assert not response

    # Too late
    bookingCode = createBooking(date.today()-timedelta(days=1),
                                date.today()-timedelta(days=1),
                                PrinterCode._XDESP95271_p,
                                NameTagType._4786103)

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
