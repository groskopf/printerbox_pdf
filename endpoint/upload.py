import os
from typing import List
from uuid import uuid4
from fastapi import File, UploadFile, APIRouter
from fastapi.staticfiles import StaticFiles
from werkzeug.utils import secure_filename
from file_path import FilePath

from site_paths import imagesPath

router = APIRouter()

router.mount('/images', StaticFiles(directory=imagesPath), name="images")


def allImageFiles():
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(imagesPath, topdown=False):
        for name in foundFiles:
            files.append(FilePath(filename=os.path.join(root, name)))

    return files


@router.get('/images', response_model=List[FilePath])
def getImageList():
    return allImageFiles()


@router.post('/images', response_model=FilePath)
async def postImageUpload(image: UploadFile = File(...)):
    filename = secure_filename(image.filename)
    filePath, fileExtention = os.path.splitext(filename)
    outputFilename = imagesPath + uuid4().hex + fileExtention
    outputFile = open(outputFilename, "wb")
    outputFile.write(image.file.read())
    outputFile.close()
    return FilePath(filename=outputFilename)
