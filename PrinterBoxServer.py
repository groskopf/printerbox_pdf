'''
Created on 19. apr. 2022

@author: paul
'''

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import List

from pdf.Layouts import NameData
from endpoint.images import postImage
from endpoint.name_tag import postNameTag
from endpoint.name_tag_sheet import postNameTagSheet

app = FastAPI()
  
app.mount('/images', StaticFiles(directory="images"), name="images")
app.mount('/printer_queue', StaticFiles(directory="printer_queue"), name="printer_queue")

@app.post('/image_upload')    
def postImageUpload(file: UploadFile):
    return postImage(file)

@app.post('/name_tag')
def nameTag(layout : str, nameData : NameData ):
    return postNameTag(layout, nameData)
    
@app.post('/name_tag_sheet')
def nameTagSheet(layout : str, nameDataList : List[NameData] ):
    return postNameTagSheet(layout, nameDataList)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


