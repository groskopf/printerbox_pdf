
from datetime import date
import json
from typing import List
from fastapi.testclient import TestClient
import pytest

from main import app
from pdf.name_tag_type import NameTagType
from printer_code import PrinterCode
from test.test_bookings import newBooking, deleteBookings
from test.test_printers import newNameTag, deleteAllNameTags
from test.test_images import deleteAllImages

client = TestClient(app)

def test_printers_ws(deleteBookings, deleteAllNameTags, deleteAllImages):

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
        with client.websocket_connect('/printers/'+ printerCode + '/ws') as websocket:
            for i in range(numOfNewNameTags):
                receivedFilename = websocket.receive_json(mode='text')
                assert any(newNameTag == receivedFilename['filename'] for newNameTag in newNameTags)