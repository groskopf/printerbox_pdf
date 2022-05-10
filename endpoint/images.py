'''
Created on 5. maj 2022

@author: paul
'''
    
from fastapi import UploadFile

from werkzeug.utils import secure_filename

    
def postImage(uploadFile: UploadFile):    
    outputFile = open("images/" + secure_filename(uploadFile.filename), "wb")
    outputFile.write(uploadFile.file.read())
    outputFile.close()
    return {"filename": uploadFile.filename}


    