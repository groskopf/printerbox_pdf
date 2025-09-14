import os
from datetime import date as date, timedelta
from re import I
from typing import List
from fastapi import status
from fastapi.testclient import TestClient
import pytest

from main import app
from pdf.name_tag_layouts import getNameTagLayouts
from site_paths import nameTagsPath
from endpoint.booking_calendar import calendar
from pdf.name_tag_type import NameTagType
from pdf.layouts import Layout
from printer_code import PrinterCode
from test.test_bookings import newBooking, deleteBooking
from test.test_images import newImage

client = TestClient(app)


def deleteAllNameTagFiles():
    for root, dirs, files in os.walk(nameTagsPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


@pytest.fixture
def deleteAllNameTags():
    deleteAllNameTagFiles()


def postNameTag(bookingCode: str):
    image = os.path.basename(newImage('./test/images/kongresartikler_men_rgba.png'))
    body = {
        "line_1": "string string string string string string string string string",
        "line_2": "string string string string string string string string string",
        "line_3": "string string string string string string string string string",
        "line_4": "string string string string string string string string string",
        "line_5": "string string string string string string string string string",
        "qr_code": "string string string string string string string string string",
        "image_name": image
    }
    response = client.post('/name_tags/' + bookingCode +
                           '?layout=' + Layout.LAYOUT_1,
                           json=body,
                           headers={'access_token': '123admin'})
    return response


def newNameTag(bookingCode: str):
    response = postNameTag(bookingCode)
    assert response.status_code == 201
    filename = response.json()['filename']
    assert filename
    return filename


def postNameTagWithLayout(bookingCode: str, layout: Layout, body = None):
    if body is None:
        image = os.path.basename(newImage('./test/images/kongresartikler_blue_man.jpg'))
        body = {
            "line_1": "Kolonne 1",
            "line_2": "Kolonne 2",
            "line_3": "Kolonne 3",
            "line_4": "Kolonne 4",
            "line_5": "Kolonne 5",
            # "line_1": "<font size=\"18\"><b>Sebastian Line 1</b></font>",
            # "line_2": "<font size=\"14\"><i>Line 2 Dekoratør</i></font>",
            # "line_3": "<font size=\"16\"><b>Line 3 FUSK A/S</b></font>",
            # "line_4": "Line 4 hello hello",
            # "line_5": "Line 5 hello hello",
            "qr_code": "kongresartikler.dk",
            "image_name": image
        }
    response = client.post('/name_tags/' + bookingCode +
                           '?layout=' + layout,
                           json=body,
                           headers={'access_token': '123admin'})
    return response


def newNameTagWithLayout(bookingCode: str, layout: Layout, body=None):
    response = postNameTagWithLayout(bookingCode, layout, body)
    assert response.status_code == 201
    filename = response.json()['filename']
    assert filename
    return filename


def test_new_name_tag(deleteBookings, deleteAllNameTags):
    for nameTagType in NameTagType:
        # Today
        bookingCode = newBooking(date.today(),
                                date.today(),
                                PrinterCode._1OPYKBGXVN_1,
                                nameTagType)

        # Create a name tag
        filename = newNameTag(bookingCode)

        # Do file exist locally
        assert os.path.exists(filename) and os.path.isfile(filename)

        # TODO can we download it?
       
        deleteBooking(bookingCode)


def test_name_tag_all_layouts(deleteBookings, deleteAllNameTags):
    body = {
        "qr_code": "kongresartikler.dk"
    }

    for kolonne in range(1, 6):
        body[f"line_{kolonne}"] = f"Kolonne {kolonne}"

        for nameTagType in NameTagType:
            # Today
            bookingCode = newBooking(date.today(),
                                    date.today(),
                                    PrinterCode._1OPYKBGXVN_1,
                                    nameTagType)

            layouts = getNameTagLayouts(nameTagType)
            for layout in layouts.layouts:
                if layout == Layout.LAYOUT_INVALID:
                    continue
                
                image : str =""
                if layout in (Layout.LAYOUT_2PB, 
                              Layout.LAYOUT_2PT, 
                              Layout.LAYOUT_2PTLQ, 
                              Layout.LAYOUT_2PTRQ, 
                              Layout.LAYOUT_2PBLQ, 
                              Layout.LAYOUT_2PBRQ, 
                              Layout.LAYOUT_3PTLQ, 
                              Layout.LAYOUT_3PTRQ, 
                              Layout.LAYOUT_3PBLQ, 
                              Layout.LAYOUT_3PBRQ, 
                              Layout.LAYOUT_3PB, 
                              Layout.LAYOUT_3PT):
                    image = os.path.basename(newImage('./test/images/big.jpg'))
                else:
                    image = os.path.basename(newImage('./test/images/small.jpg'))
                    
                body["image_name"] = image

                # Create a name tag
                filename = newNameTagWithLayout(bookingCode, layout, body)

                # Do file exist locally
                assert os.path.exists(filename) and os.path.isfile(filename)

            deleteBooking(bookingCode)

def test_name_tag_vcard(deleteBookings, deleteAllNameTags):
    body = {
        "qr_code": "BEGIN:VCARD\nVERSION:3.0\nN:Groskopf;A. D. Valdal\nORG:Kongresartikler.dk\nTITLE:CEO\nEMAIL:info@kongresartiler.dk\nTEL:+4543623210\nURL:www.kongresartikler.dk\nEND:VCARD"
    }

    for kolonne in range(1, 6):
        body[f"line_{kolonne}"] = f"Kolonne {kolonne}"

        for nameTagType in NameTagType:
            # Today
            bookingCode = newBooking(date.today(),
                                    date.today(),
                                    PrinterCode._1OPYKBGXVN_1,
                                    nameTagType)
            for layout in (Layout.LAYOUT_2QT,):

                # Create a name tag
                filename = newNameTagWithLayout(bookingCode, layout, body)

                # Do file exist locally
                assert os.path.exists(filename) and os.path.isfile(filename)

            deleteBooking(bookingCode)

def test_booking_wrong_dates(deleteBookings, deleteAllNameTags, deleteAllImages):
    # Too early
    bookingCode = newBooking(date.today()+timedelta(days=1),
                             date.today()+timedelta(days=1),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    # Create a name tag
    response = postNameTag(bookingCode)
    assert response.status_code == 400

    # Too late
    bookingCode = newBooking(date.today()-timedelta(days=1),
                             date.today()-timedelta(days=1),
                             PrinterCode._1OPYKBGXVN_1,
                             NameTagType._4786103)

    # Create a name tag
    response = postNameTag(bookingCode)
    assert response.status_code == 400


def test_bad_booking(deleteBookings, deleteAllNameTags):
    bookingCode = 'FAKE_BOOKING'

    # Create a name tag
    response = postNameTag(bookingCode)
    assert response.status_code == status.HTTP_404_NOT_FOUND


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
        response = client.get('/name_tags/' + bookingCode,
                              headers={'access_token': '123admin'})
        assert response.status_code == 200
        filenames = response.json()

        numFundNameTags = len(filenames)
        assert numFundNameTags == numOfNewNameTags

        # Compare the list with the output
        newNameTags.sort()
        sortedFileNames = sorted(filenames, key=lambda d: d['filename'])
        for i in range(numFundNameTags):
            assert sortedFileNames[i]['filename'] == newNameTags[i]

    # Test they disappear again
    deleteAllNameTagFiles()

    for printerCode in PrinterCode:
        response = client.get('/name_tags/' + calendar.getPrinterBooking(printerCode).booking_code,
                              headers={'access_token': '123admin'})
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

        numOfNewNameTags = 5
        newNameTags: List[str] = []

        # Create some nametags
        for i in range(numOfNewNameTags):
            newNameTags.append(newNameTag(bookingCode))

        # Try delete all name tags
        response = client.delete('/name_tags/' + bookingCode,
                                 headers={'access_token': '123admin'})
        assert response.status_code == 200

        # Test they all disappear again
        response = client.get('/name_tags/' + calendar.getPrinterBooking(printerCode).booking_code,
                              headers={'access_token': '123admin'})
        assert response.status_code == 200
        filenames = response.json()
        assert len(filenames) == 0


def test_delete_name_tag(deleteBookings, deleteAllNameTags, deleteAllImages):

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
        response = client.get('/name_tags/' + calendar.getPrinterBooking(printerCode).booking_code,
                              headers={'access_token': '123admin'})
        assert response.status_code == 200
        filenames = response.json()

        # Try delete all name tags
        for filename in filenames:
            response = client.delete(filename['filename'],
                                     headers={'access_token': '123admin'})
            assert response.status_code == 200

    # Test they all disappear again
    for printerCode in PrinterCode:
        response = client.get('/name_tags/' + calendar.getPrinterBooking(printerCode).booking_code,
                              headers={'access_token': '123admin'})
        assert response.status_code == 200
        filenames = response.json()
        assert len(filenames) == 0


def test_wrong_layout_name_tag_sheet(deleteBookings, deleteAllNameTags, deleteAllImages):
    bookingCode = newBooking(
        date.today(),
        date.today(),
        PrinterCode._8SCNWZUF9M_8,
        NameTagType._4786103)
    image = os.path.basename(newImage('./test/images/kongresartikler_men_rgba.png'))
    body = {
        "line_1": "string",
        "line_2": "string",
        "line_3": "string",
        "line_4": "string",
        "line_5": "string",
        "qr_code": "string",
        "image_name": image
    }
    response = client.post('/name_tags/' + bookingCode +
                           '?layout=' + Layout.LAYOUT_INVALID,
                           json=body,
                           headers={'access_token': '123admin'})
    assert response.status_code == 400


def test_post_name_tags_access_rights(deleteBookings):
    bookingCode = newBooking(
        date.today(),
        date.today(),
        PrinterCode._8SCNWZUF9M_8,
        NameTagType._4786103)
    image = os.path.basename(newImage('./test/images/kongresartikler_men_rgba.png'))
    body = {
        "line_1": "string",
        "line_2": "string",
        "line_3": "string",
        "line_4": "string",
        "line_5": "string",
        "qr_code": "string",
        "image_name": image
    }

    response = client.post('/name_tags/' + bookingCode + '?layout=' + Layout.LAYOUT_1,
                           json=body,
                           headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post('/name_tags/' + bookingCode + '?layout=' + Layout.LAYOUT_1,
                           json=body,
                           headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post('/name_tags/' + bookingCode + '?layout=' + Layout.LAYOUT_1,
                           json=body,
                           headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post('/name_tags/' + bookingCode + '?layout=' + Layout.LAYOUT_1,
                           json=body,
                           headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post('/name_tags/' + bookingCode + '?layout=' + Layout.LAYOUT_1,
                           json=body)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_name_tags_printer_code_access_rights(deleteBookings):
    printerCode = PrinterCode._8SCNWZUF9M_8
    bookingCode = newBooking(
        date.today(),
        date.today(),
        printerCode,
        NameTagType._4786103)
    newNameTag(bookingCode)
    response = client.get('/name_tags/' + bookingCode +
                          '?access_token=123admin')
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/name_tags/' + bookingCode)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/name_tags/' + bookingCode,
                          headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/name_tags/' + bookingCode,
                          headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/name_tags/' + bookingCode,
                          headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/name_tags/' + bookingCode,
                          headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_name_tags_printer_code_access_rights(deleteBookings):
    printerCode = PrinterCode._8SCNWZUF9M_8
    bookingCode = newBooking(
        date.today(),
        date.today(),
        printerCode,
        NameTagType._4786103)
    newNameTag(bookingCode)
    response = client.delete('/name_tags/' + bookingCode)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.delete('/name_tags/' + bookingCode,
                             headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.delete('/name_tags/' + bookingCode,
                             headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK
    response = client.delete('/name_tags/' + bookingCode,
                             headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_200_OK
    response = client.delete('/name_tags/' + bookingCode,
                             headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_name_tags_printer_code_file_name_access_rights(deleteBookings):
    printerCode = PrinterCode._8SCNWZUF9M_8
    bookingCode = newBooking(
        date.today(),
        date.today(),
        printerCode,
        NameTagType._4786103)

    filename = newNameTag(bookingCode)
    response = client.get(filename)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get(filename,
                          headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    filename = newNameTag(bookingCode)
    response = client.get(filename,
                          headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK

    filename = newNameTag(bookingCode)
    response = client.get('/name_tags/' + bookingCode,
                          headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK

    filename = newNameTag(bookingCode)
    response = client.get('/name_tags/' + bookingCode,
                          headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_200_OK


def test_delete_name_tags_printer_code_file_name_access_rights(deleteBookings):
    printerCode = PrinterCode._8SCNWZUF9M_8
    bookingCode = newBooking(
        date.today(),
        date.today(),
        printerCode,
        NameTagType._4786103)

    filename = newNameTag(bookingCode)
    response = client.delete(filename)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.delete(filename,
                             headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    filename = newNameTag(bookingCode)
    response = client.delete(filename,
                             headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK

    filename = newNameTag(bookingCode)
    response = client.delete('/name_tags/' + bookingCode,
                             headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK

    filename = newNameTag(bookingCode)
    response = client.delete('/name_tags/' + bookingCode,
                             headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_200_OK
