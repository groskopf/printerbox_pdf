from datetime import date as date
import uvicorn
from fastapi import FastAPI

from site_paths import printersPath, labelsPath
from endpoint import images, bookings, labels, printers, printers_ws 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "*",   
    #  FIXME add more origins 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(images.router, prefix='/images', tags=['images'])
app.include_router(bookings.router, prefix='/bookings', tags=['admin'])
app.include_router(labels.router, prefix='/labels', tags=['labels-designer'])
app.include_router(printers.router, prefix='/printers', tags=['printers'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
