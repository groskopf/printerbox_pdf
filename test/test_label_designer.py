import os
import pytest
from fastapi.testclient import TestClient

from main import app
from file_path import FilePath
from site_paths import labelsPath
from test.test_upload import uploadImage

client = TestClient(app)


@pytest.fixture
def removeOldSheets():
    for root, dirs, files in os.walk(labelsPath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def createNameTagSheet():
    image1 = os.path.basename(uploadImage('./test/images/Kongresartikler.jpg'))
    image2 = os.path.basename(uploadImage('./test/images/logo.jpg'))
    body = [
        {"name": "string",
         "description1": "string",
         "description2": "string",
         "description3": "string",
         "description4": "string",
         "imageName": image1},
        {"name": "string",
         "description1": "string",
         "description2": "string",
         "description3": "string",
         "description4": "string",
         "imageName": image2}
    ]
    response = client.post('/label_designer/456090/layout_1', json=body)
    return response


def test_new_name_tag_sheet(removeOldSheets):
    for i in range(10):
        response = createNameTagSheet()
        assert response.status_code == 201

        # Do file exist locally
        filename = response.json()['filename']
        assert os.path.exists(filename) and os.path.isfile(filename)

        # TODO can we download it?


