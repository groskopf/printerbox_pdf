from fastapi import File, UploadFile, APIRouter
from fastapi.staticfiles import StaticFiles
from werkzeug.utils import secure_filename

from filePaths import imagesPath

router = APIRouter()
    
router.mount('/images', StaticFiles(directory=imagesPath), name="images")

@router.post('/images')
async def postImageUpload(file: UploadFile = File(...)):
    outputFile = open(imagesPath + secure_filename(file.filename), "wb")
    outputFile.write(file.file.read())
    outputFile.close()
    return {"filename": file.filename}


    