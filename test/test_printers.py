import os
from datetime import date as date, timedelta
from fastapi.testclient import TestClient
import pytest

from main import app
from site_paths import printersPath
from pdf.name_tag_type import NameTagType
from pdf.layouts import Layout
from printer_code import PrinterCode
from test.test_bookings import newBooking, deleteBookings
from test.test_images import deleteAllImages, newImage

client = TestClient(app)


def deleteAllNameTagFiles():
    for root, dirs, files in os.walk(printersPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


@pytest.fixture
def deleteAllNameTags():
    deleteAllNameTagFiles()


def postNameTag(bookingCode: str):
    image = os.path.basename(newImage('./test/images/logo.jpg'))
    body = {"name": "string",
            "description1": "string",
            "description2": "string",
            "description3": "string",
            "description4": "string",
            "imageName": image}
    response = client.post('/printers/?booking_code=' + bookingCode +
                           '&layout=' + Layout.LAYOUT_1,
                           json=body)
    return response


def newNameTag(bookingCode: str):
    response = postNameTag(bookingCode)
    assert response.status_code == 201
    filename = response.json()['filename']
    assert filename
    return filename


def test_new_name_tag(deleteBookings, deleteAllNameTags):
    # Today
    bookingCode = newBooking(date.today(),
                             date.today(),
                             PrinterCode._XDESP95271_p,
                             NameTagType._4786103)

    # Create a name tag
    filename = newNameTag(bookingCode)

    # Do file exist locally
    assert os.path.exists(filename) and os.path.isfile(filename)

    # TODO can we download it?


def test_booking_wrong_dates(deleteBookings, deleteAllNameTags, deleteAllImages):
    # Too early
    bookingCode = newBooking(date.today()+timedelta(days=1),
                             date.today()+timedelta(days=1),
                             PrinterCode._XDESP95271_p,
                             NameTagType._4786103)

    # Create a name tag
    response = postNameTag(bookingCode)
    assert response.status_code == 400
    assert not response

    # Too late
    bookingCode = newBooking(date.today()-timedelta(days=1),
                             date.today()-timedelta(days=1),
                             PrinterCode._XDESP95271_p,
                             NameTagType._4786103)

    # Create a name tag
    response = postNameTag(bookingCode)
    assert response.status_code == 400
    assert not response


def test_bad_booking(deleteBookings, deleteAllNameTags):
    bookingCode = 'FAKE_BOOKING'

    # Create a name tag
    response = postNameTag(bookingCode)
    assert response.status_code == 404
    assert not response


def test_get_name_tags(deleteBookings, deleteAllNameTags, deleteAllImages):

    for printerCode in PrinterCode:
        bookingCode = newBooking(
            date.today(),
            date.today(),
            printerCode,
            NameTagType._4786103)

        numOfNewNameTags = 5
        newNameTags: List[str] = []

        # Create some nametags
        for i in range(numOfNewNameTags):
            newNameTags.append(newNameTag(bookingCode))

        # Get the list
        response = client.get('/printers/' + printerCode)
        assert response.status_code == 200
        filenames = response.json()

        numFundNamesTags = len(filenames)
        assert numFundNamesTags == numOfNewNameTags

        # Compare the list with the output
        newNameTags.sort()
        sortedFileNames = sorted(filenames, key=lambda d: d['filename'])
        for i in range(numFundNamesTags):
            assert sortedFileNames[i]['filename'] == newNameTags[i]

    # Test they disappear again
    deleteAllNameTagFiles()

    for printerCode in PrinterCode:
        response = client.get('/printers/' + printerCode)
        assert response.status_code == 200
        filenames = response.json()
        assert len(filenames) == 0


def test_delete_name_tags(deleteBookings, deleteAllNameTags, deleteAllImages):

    for printerCode in PrinterCode:
        # Create a booking on the printer
        bookingCode = newBooking(
            date.today(),
            date.today(),
            printerCode,
            NameTagType._4786103)

        # Create some name tags
        for i in range(5):
            newNameTag(bookingCode)

    for printerCode in PrinterCode:
        # Get the name tags
        response = client.get('/printers/' + printerCode)
        assert response.status_code == 200
        filenames = response.json()

        # Try delete all name tags
        for filename in filenames:
            response = client.delete(filename['filename'])
            assert response.status_code == 200

    # Test they all disappear again
    for printerCode in PrinterCode:
        response = client.get('/printers/' + printerCode)
        assert response.status_code == 200
        filenames = response.json()
        assert len(filenames) == 0
