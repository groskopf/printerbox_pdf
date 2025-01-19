import os
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from endpoint.authentication import AccessScope

from main import app
from file_path import FilePath
from site_paths import sheetsPath
from test.test_images import newImage

client = TestClient(app)


@pytest.fixture
def removeOldSheets():
    for root, dirs, files in os.walk(sheetsPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def newSheet():
    image1 = os.path.basename(newImage('./test/images/kongresartikler_men_rgba.png'))
    image2 = os.path.basename(newImage('./test/images/kongresartikler_men.jpg'))
    body = [
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "image_name": image1
        },
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "image_name": image2
        },
    ]
    response = client.post('/sheets/?sheet_type=456090&layout=layout_1',
                           json=body,
                           headers={'access_token': '789conference'})
    return response


def getSheets():
    # Get the list of images
    response = client.get('/sheets/', headers={'access_token': '123admin'})
    assert response.status_code == 200
    filenames = response.json()
    return filenames


def test_new_sheet(removeOldSheets):
    for i in range(10):
        response = newSheet()
        assert response.status_code == 201

        # Do file exist locally
        filename = response.json()['filename']
        assert os.path.exists(filename) and os.path.isfile(filename)

    # Get the list of images
    filenames = getSheets()
    assert 10 == len(filenames)


def test_get_sheet():
    response = newSheet()
    assert response.status_code == 201

    filename = response.json()['filename']

    response = client.get(filename, headers={'access_token': '123admin'})
    assert response.status_code == 200

def test_delete_sheet():
    response = newSheet()
    assert response.status_code == 201
    filename = response.json()['filename']

    response = client.delete(filename, headers={'access_token': '123admin'})
    assert response.status_code == 200
    assert filename == response.json()['filename']

    # Are they deleted
    assert not os.path.exists(filename)


def test_wrong_layout_sheet(removeOldSheets):
    image = os.path.basename(newImage('./test/images/kongresartikler_men.jpg'))
    body = [
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "image_name": image
        },
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "image_name": image
        },
    ]
    response = client.post('/sheets/?sheet_type=456090&layout=invalid',
                           json=body,
                           headers={'access_token': '789conference'})
    assert response.status_code == 400


def test_get_sheets_access_rights():
    response = client.get('/sheets/')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/', headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/sheets/', headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/', headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_sheets_access_rights():
    image1 = os.path.basename(newImage('./test/images/kongresartikler_men_rgba.png'))
    image2 = os.path.basename(newImage('./test/images/kongresartikler_men.jpg'))
    body = [
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "image_name": image1
        },
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "image_name": image2
        },
    ]
    response = client.post('/sheets/?sheet_type=456090&layout=layout_1', json=body)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post('/sheets/?sheet_type=456090&layout=layout_1', json=body, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post('/sheets/?sheet_type=456090&layout=layout_1', json=body, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post('/sheets/?sheet_type=456090&layout=layout_1', json=body, headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_sheet_access_rights():
    response = newSheet()
    assert response.status_code == 201

    filename = response.json()['filename']

    response = client.get(filename)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get(filename, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get(filename, headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get(filename, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_sheet_access_rights():
    response = newSheet()
    assert response.status_code == 201
    filename = response.json()['filename']

    response = client.get(filename)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get(filename, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.get(filename, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    
    response = newSheet()
    assert response.status_code == 201
    filename = response.json()['filename']
    response = client.get(filename, headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_200_OK

def test_access_key_checker():
    response = client.get('/sheets/')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/', headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/sheets/', headers={'access_token': 'printer_p'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/', headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/', headers={'access_token': 'printer_p789conference'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.get('/sheets/?access_token=12341234')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/?access_token=123admin')
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/sheets/?access_token=printer_p')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('/sheets/?access_token=789conference')
    assert response.status_code == status.HTTP_403_FORBIDDEN
