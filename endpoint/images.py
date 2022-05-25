from http.client import HTTPException
import os
from typing import List
from uuid import uuid4
from fastapi import File, UploadFile, APIRouter, status
from fastapi.responses import FileResponse
from werkzeug.utils import secure_filename
from details import Details
from file_path import FilePath

from site_paths import imagesPath

router = APIRouter()

def allImageFiles():
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(imagesPath, topdown=False):
        for name in foundFiles:
            files.append(FilePath(filename=os.path.join(root, name)))

    return files


@router.get('/', response_model=List[FilePath])
def get_images():
    return allImageFiles()

@router.post('/', response_model=FilePath)
async def new_image(image: UploadFile = File(...)):
    filename = secure_filename(image.filename)
    filePath, fileExtention = os.path.splitext(filename)
    outputFilename = imagesPath + uuid4().hex + fileExtention
    outputFile = open(outputFilename, "wb")
    outputFile.write(image.file.read())
    outputFile.close()
    return FilePath(filename=outputFilename)

@router.get('/{filename}',
            response_model=List[FilePath],
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_image(filename : str):
    imageFilename = imagesPath + secure_filename(filename)
    if os.path.exists(imageFilename) and os.path.isfile(imageFilename):
        os.remove(imageFilename)
        return FilePath(filename=imageFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

@router.delete('/{filename}',
            response_model=FilePath,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def delete_image(filename: str):
    imageFilename = imagesPath + secure_filename(filename)
    if os.path.exists(imageFilename) and os.path.isfile(imageFilename):
        os.remove(imageFilename)
        return FilePath(filename=filename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


