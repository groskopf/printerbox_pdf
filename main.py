from datetime import date as date
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from endpoint import upload, bookings, onsite_print, label_designer

app = FastAPI()

app.mount('/queues', StaticFiles(directory="./queues"),  name="queues")
app.mount('/labels', StaticFiles(directory="./labels"),  name="labels")

app.include_router(upload.router, prefix='/upload')
app.include_router(bookings.router, prefix='/bookings', tags=['admin'])
app.include_router(onsite_print.router, prefix='/onsite_print', tags=['onsite-print'])
app.include_router(label_designer.router, prefix='/label_designer', tags=['label-designer'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
