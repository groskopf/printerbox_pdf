import os
from typing import List
from uuid import uuid4
from fastapi import File, UploadFile, APIRouter, status, HTTPException, Security
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKey
from werkzeug.utils import secure_filename
from details import Details
from file_path import FilePath

from site_paths import imagesPath
from endpoint.authentication import AccessScope, authenticate_api_key

router = APIRouter()

def allImageFiles():
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(imagesPath, topdown=False):
        for name in foundFiles:
            files.append(FilePath(filename=os.path.join(root, name)))

    return files


@router.get('/', response_model=List[FilePath])
def get_images(api_key: APIKey = Security(authenticate_api_key, scopes=[])):
    return allImageFiles()

@router.post('/', response_model=FilePath)
async def new_image(image: UploadFile = File(...),
    api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    filename = secure_filename(image.filename)
    filePath, fileExtention = os.path.splitext(filename)
    outputFilename = imagesPath + uuid4().hex + fileExtention
    outputFile = open(outputFilename, "wb")
    outputFile.write(image.file.read())
    outputFile.close()
    return FilePath(filename=outputFilename)

@router.get('/{filename}',
            response_class=FileResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_image(filename : str,
    api_key: APIKey = Security(authenticate_api_key, scopes=[])):
    imageFilename = imagesPath + secure_filename(filename)
    if os.path.exists(imageFilename) and os.path.isfile(imageFilename):
        return FileResponse(path=imageFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Image not found")

@router.delete('/{filename}',
            response_model=FilePath,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def delete_image(filename: str,
    api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    imageFilename = imagesPath + secure_filename(filename)
    if os.path.exists(imageFilename) and os.path.isfile(imageFilename):
        os.remove(imageFilename)
        return FilePath(filename=filename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


