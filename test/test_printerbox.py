import os
from datetime import date as date, timedelta
from typing import List
from fastapi.testclient import TestClient
import pytest

from main import app
from site_paths import imagesPath
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode
from test.test_bookings import createBooking, clearBookingList
from test.test_onsite_print import deleteAllFilesInQueues, newNameTag, removeOldPrints
from test.test_upload import removeOldImages

client = TestClient(app)


def test_get_name_tags(clearBookingList, removeOldPrints, removeOldImages):

    for printerCode in PrinterCode:
        bookingCode = createBooking(
            date.today(),
            date.today(),
            printerCode,
            NameTagType._4786103)

        numOfNewNameTags = 10
        newNameTags : List[str] = []
        
        # Create some nametags
        for i in range(numOfNewNameTags):
            newNameTags.append(newNameTag(bookingCode))

        # Get the list
        response = client.get('/printerbox/' + printerCode)
        assert response.status_code == 200
        fileNames = response.json()

        numFundNamesTags = len(fileNames)
        assert numFundNamesTags == numOfNewNameTags 

        # Compare the list with the output
        newNameTags.sort()
        sortedFileNames = sorted(fileNames, key=lambda d: d['filename'])
        for i in range(numFundNamesTags):
            assert sortedFileNames[i]['filename'] == newNameTags[i]

    # Test they disappear again
    deleteAllFilesInQueues()

    for printerCode in PrinterCode:
        response = client.get('/printerbox/' + printerCode)
        assert response.status_code == 200
        fileNames = response.json()
        assert len(fileNames) == 0