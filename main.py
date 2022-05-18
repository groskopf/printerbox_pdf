'''
Created on 19. apr. 2022

@author: paul
'''

import uvicorn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from typing import List

from endpoint.name_data import NameData
from endpoint.images import postImage
from endpoint.name_tag import postNameTag
from endpoint.name_tag_sheet import postNameTagSheet
from pdf.layouts import Layout

app = FastAPI()

app.mount('/images', StaticFiles(directory="./images"), name="images")
app.mount('/printer_queue', StaticFiles(directory="./printer_queue"), name="printer_queue")

@app.post('/image_upload')    
def postImageUpload(file: UploadFile = File(...)):
    return postImage(file)

@app.post('/name_tag')
def nameTag(layout : Layout, nameData : NameData ):
    return postNameTag(layout, nameData)
    
@app.post('/name_tag_sheet')
def nameTagSheet(layout : str, nameDataList : List[NameData] ):
    return postNameTagSheet(layout, nameDataList)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


