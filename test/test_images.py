import os
from typing import List
import pytest
from datetime import date as date
from fastapi import Security, status
from fastapi.testclient import TestClient

from main import app
from site_paths import imagesPath
from test.test_bookings import newBooking, deleteBookings

client = TestClient(app)


@pytest.fixture
def deleteAllImages():
    for root, dirs, files in os.walk(imagesPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def newImage(imageName: str):
    with open(imageName, "rb") as f:
        response = client.post('/images/',
                               files={"image": (imageName, f, "image/jpeg")},
                               headers={'access_token': '123admin'})
        assert response.status_code == 200
        body = response.json()
        newImageName = body['filename']
        assert os.path.basename(imageName) != os.path.basename(newImageName)
        return newImageName


def newImages(imageList: List[str]):
    # Create new images
    newNameImageList = []
    for imageName in imageList:
        newImageName = newImage(imageName)
        newNameImageList.append(newImageName)

    # Are they saved
    for imageName in newNameImageList:
        assert os.path.exists(imageName)
        assert os.path.isfile(imageName)

    return newNameImageList


def getImages():
    # Get the list of images
    response = client.get('/images', headers={'access_token': '123admin'})
    assert response.status_code == 200
    imageNames = response.json()
    return imageNames


def test_upload_image(deleteAllImages):

    newImageList = newImages(
        ['./test/images/logo.jpg', './test/images/Kongresartikler.png'])

    imageNames = getImages()
    assert len(newImageList) == len(imageNames)

    for imageName in imageNames:
        if imageName['filename'] not in newImageList:
            assert False


def test_delete_image(deleteAllImages):
    newImageList = newImages(
        ['./test/images/logo.jpg', './test/images/Kongresartikler.png'])

    # Delete images again
    for imageName in newImageList:
        response = client.delete(imageName, headers={'access_token': '123admin'})
        assert response.status_code == 200
        fileName = response.json()['filename']

    # Are they deleted
    for imageName in newImageList:
        assert not os.path.exists(imageName)

    # Get the list of images
    imageList = getImages()
    assert 0 == len(imageList)


def test_get_images_access_rights(deleteAllImages):
    response = client.get('/images', headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/images', headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/images', headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/images', headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_post_images_access_right(deleteAllImages):
    imageName = './test/images/logo.jpg'
    with open(imageName, "rb") as f:
        response = client.post('/images/',
                                files={"image": (imageName, f, "image/jpeg")},
                                headers={'access_token': '123admin'})
        assert response.status_code == status.HTTP_200_OK
        response = client.post('/images/',
                                files={"image": (imageName, f, "image/jpeg")},
                                headers={'access_token': 'printer_p'})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = client.post('/images/',
                                files={"image": (imageName, f, "image/jpeg")},
                                headers={'access_token': '789conference'})
        assert response.status_code == status.HTTP_200_OK
        response = client.post('/images/',
                                files={"image": (imageName, f, "image/jpeg")},
                                headers={'access_token': 'xyzbooking'})
        assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_image_access_right(deleteAllImages):
    imageName = newImage('./test/images/logo.jpg')

    response = client.get(imageName, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get(imageName, headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get(imageName, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get(imageName, headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

        

def test_delete_image_access_right(deleteAllImages):
    imageName = newImage('./test/images/logo.jpg')

    response = client.delete(imageName, headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.delete(imageName, headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.delete(imageName, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    
    imageName = newImage('./test/images/logo.jpg')
    
    response = client.delete(imageName, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK

        