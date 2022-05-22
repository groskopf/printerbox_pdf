import os
from datetime import date as date, timedelta
from fastapi.testclient import TestClient
import pytest

from main import app
from filePaths import imagesPath
from printer_code import PrinterCode
from test.test_bookings import createBooking, clearBookingList

client = TestClient(app)

@pytest.fixture
def removeOldImages():
    for root, dirs, files in os.walk(imagesPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def uploadImage(imageName : str):
    with open(imageName, "rb") as f:
        response = client.post("/upload/images", files={"file": (os.path.basename(imageName), f, "image/jpeg")})

def test_upload_image(removeOldImages):
    imageList = ['./test/images/logo.jpg', './test/images/Kongresartikler.jpg' ]
    
    for imageName in imageList:
        uploadImage(imageName)

    for imageName in imageList:
        uploadName = imagesPath + os.path.basename(imageName)
        assert os.path.exists(uploadName)    
        assert os.path.isfile(uploadName)    

