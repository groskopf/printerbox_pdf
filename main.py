from datetime import date as date
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from site_paths import queuesPath, labelsPath
from endpoint import upload, bookings, label_designer, onsite_print, printerbox 

app = FastAPI()

app.mount('/queues', StaticFiles(directory=queuesPath),  name="queues")
app.mount('/labels', StaticFiles(directory=labelsPath),  name="labels")

app.include_router(upload.router, prefix='/upload')
app.include_router(bookings.router, prefix='/bookings', tags=['admin'])
app.include_router(label_designer.router, prefix='/label_designer', tags=['label-designer'])
app.include_router(onsite_print.router, prefix='/onsite_print', tags=['onsite-print'])
app.include_router(printerbox.router, prefix='/printerbox', tags=['printerbox'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
