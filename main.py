import uvicorn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from typing import List

from endpoint.name_data import NameData
from endpoint.images import postImage
from endpoint.name_tag import postNameTag
from endpoint.name_tag_sheet import postNameTagSheet
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf.name_tag_sheet_type import NameTagSheetType

app = FastAPI()

app.mount('/images', StaticFiles(directory="./images"), name="images")
app.mount('/printer_queue', StaticFiles(directory="./printer_queue"),
          name="printer_queue")


@app.post('/image_upload')
def postImageUpload(file: UploadFile = File(...)):
    return postImage(file)


@app.post('/name_tag/{name_tag_type}/{layout}')
def nameTag(nameTagType: NameTagType, layout: Layout, nameData: NameData):
    return postNameTag(nameTagType, layout, nameData)


@app.post('/name_tag_sheet{name_tag_sheet_type}/{layout}')
def nameTagSheet(nameTagSheetType: NameTagSheetType, layout: Layout, nameDataList: List[NameData]):
    return postNameTagSheet(nameTagSheetType, layout, nameDataList)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
