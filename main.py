from datetime import date as date
import uvicorn
from fastapi import FastAPI

from endpoint import endpoint_bookings, endpoint_images, endpoint_layouts, endpoint_name_tags, endpoint_sheets
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


app.include_router(endpoint_images.router, prefix='/images', tags=['images'])
app.include_router(endpoint_bookings.router, prefix='/bookings', tags=['bookings'])
app.include_router(endpoint_sheets.router, prefix='/sheets', tags=['sheets'])
app.include_router(endpoint_name_tags.router, prefix='/name_tags', tags=['name_tags'])
app.include_router(endpoint_layouts.router, prefix='/layouts', tags=['layouts'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
