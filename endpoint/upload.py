from fastapi import File, UploadFile, APIRouter
from fastapi.staticfiles import StaticFiles
from werkzeug.utils import secure_filename
from endpoint.printerbox import Filename

from filePaths import imagesPath

router = APIRouter()
    
router.mount('/images', StaticFiles(directory=imagesPath), name="images")

@router.post('/images', response_model=Filename)
async def postImageUpload(file: UploadFile = File(...)):
    filename = imagesPath + secure_filename(file.filename)
    outputFile = open(filename, "wb")
    outputFile.write(file.file.read())
    outputFile.close()
    return Filename(filename=filename)


    