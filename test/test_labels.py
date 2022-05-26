import os
import pytest
from fastapi.testclient import TestClient

from main import app
from file_path import FilePath
from site_paths import labelsPath
from test.test_images import newImage

client = TestClient(app)


@pytest.fixture
def removeOldSheets():
    for root, dirs, files in os.walk(labelsPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def newNameTagSheet():
    image1 = os.path.basename(newImage('./test/images/Kongresartikler.jpg'))
    image2 = os.path.basename(newImage('./test/images/logo.jpg'))
    body = [
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "imageName": image1
        },
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "imageName": image2
        },
    ]
    response = client.post(
        '/labels/?name_tag_sheet_type=456090&layout=layout_1', json=body)
    return response


def getNameTagSheets():
    # Get the list of images
    response = client.get('/labels/')
    assert response.status_code == 200
    filenames = response.json()
    return filenames


def test_new_name_tag_sheet(removeOldSheets):
    for i in range(10):
        response = newNameTagSheet()
        assert response.status_code == 201

        # Do file exist locally
        filename = response.json()['filename']
        assert os.path.exists(filename) and os.path.isfile(filename)

    # Get the list of images
    filenames = getNameTagSheets()
    assert 10 == len(filenames)


def test_get_name_tag_sheet():
    assert True
    # TODO can we download it?


def test_delete_name_tag_sheet():
    response = newNameTagSheet()
    assert response.status_code == 201
    filename = response.json()['filename']

    response = client.delete(filename)
    assert response.status_code == 200
    assert filename == response.json()['filename']

    # Are they deleted
    assert not os.path.exists(filename)

def test_wrong_layout_name_tag_sheet(removeOldSheets):
    image = os.path.basename(newImage('./test/images/logo.jpg'))
    body = [
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "imageName": image
        },
        {
            "line_1": "string",
            "line_2": "string",
            "line_3": "string",
            "line_4": "string",
            "line_5": "string",
            "qr_code": "string",
            "imageName": image
        },
    ]
    response = client.post('/labels/?name_tag_sheet_type=456090&layout=invalid', json=body)
    assert response.status_code == 400

