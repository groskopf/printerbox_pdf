import os
from datetime import date as date, timedelta
from fastapi.testclient import TestClient
import pytest

from main import app
from site_paths import imagesPath
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


def uploadImage(imageName: str):
    with open(imageName, "rb") as f:
        response = client.post(
            "/upload/images", files={"image": (os.path.basename(imageName), f, "image/jpeg")})
        assert response.status_code == 200
        body = response.json()
        newImageName = body['filename']
        assert os.path.basename(imageName) != os.path.basename(newImageName)
        return newImageName


def test_upload_image(removeOldImages):
    imageList = ['./test/images/logo.jpg', './test/images/Kongresartikler.jpg']

    newNameImageList = []
    for imageName in imageList:
        newNameImageList.append(uploadImage(imageName))

    for imageName in newNameImageList:
        assert os.path.exists(imageName)
        assert os.path.isfile(imageName)

    # Get the list of images
    response = client.get('/upload/images/')
    assert response.status_code == 200
    fileNames = response.json()

    numFundNames = len(fileNames)
    assert numFundNames == len(imageList)
