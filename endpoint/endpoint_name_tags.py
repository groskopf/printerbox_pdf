import os
from typing import List
from uuid import uuid4
from datetime import date as date
from fastapi import HTTPException, status, Security
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKey
from werkzeug.utils import secure_filename
from file_path import FilePath
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf import name_tag_4786103

from details import Details
from pdf.name_tag_layouts import getNameTagLayouts
from site_paths import imagesPath, nameTagsPath
from endpoint.endpoint_bookings import calendar
from endpoint.endpoint_bookings import Booking
from endpoint.name_tags_ws import getFilesInPrinterQueue, deleteFilesInPrinterQueue, wsConnectionManager, router
from endpoint.authentication import AccessScope, authenticate_api_key
from name_data import NameData


def checkImageFileExist(nameData: NameData):
    imageName = nameData.image_name
    if imageName and len(imageName):
        imageName = imagesPath + secure_filename(imageName)
        if not os.path.exists(imageName) or not os.path.isfile(imageName):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")


def findBooking(bookingCode):
    booking: Booking = calendar.getBooking(bookingCode)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    today = date.today()  # FIXME today is not working correctly
    if booking.start_date > today or today > booking.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Booking not valid today")
    return booking.printer_code, booking.name_tag_type


@router.post('/{booking_code}',
             response_model=FilePath,
             status_code=status.HTTP_201_CREATED,
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": Details},
                 status.HTTP_404_NOT_FOUND: {"model": Details}
             })
async def new_name_tag(booking_code: str, layout: Layout, name_data: NameData,
                       api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._CONFERENCE])):
    checkImageFileExist(name_data)

    printer_code, nametag_type = findBooking(booking_code)

    if layout not in getNameTagLayouts(nametag_type).layouts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name tag layout not supported")

    outputPath = nameTagsPath + booking_code + '/'
    output_filename = outputPath + nametag_type + '_' + uuid4().hex + '.pdf'

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    match nametag_type:
        case NameTagType._4786103:
            name_tag_4786103.create(output_filename, layout, name_data)
        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="NameTagType not supported")

    response = FilePath(filename=output_filename)

    await wsConnectionManager.sendToPrinter(booking_code, response.model_dump_json())

    return response


@router.get('/{booking_code}', response_model=List[FilePath])
def get_name_tags(booking_code: str,
                  api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER, AccessScope._CONFERENCE])):
    return getFilesInPrinterQueue(booking_code)


@router.delete('/{booking_code}', response_model=List[FilePath])
def get_name_tags(booking_code: str,
                  api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER, AccessScope._CONFERENCE])):
    return deleteFilesInPrinterQueue(booking_code)


@router.get('/{booking_code}/{filename}',
            response_class=FileResponse,
            responses={
                status.HTTP_404_NOT_FOUND: {"model": Details},
            })
def get_name_tag(booking_code: str, filename: str,
                 api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER, AccessScope._CONFERENCE])):
    securedFileName = secure_filename(filename)
    nameTagFilename = nameTagsPath + booking_code + \
        '/' + os.path.basename(securedFileName)

    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        return FileResponse(path=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Name tag not found")


@router.delete('/{booking_code}/{filename}',
               response_model=FilePath,
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": Details},
               })
def delete_name_tag(booking_code: str, filename: str,
                    api_key: APIKey = Security(authenticate_api_key, scopes=[AccessScope._PRINTER, AccessScope._CONFERENCE])):
    securedFileName = secure_filename(filename)
    nameTagFilename = nameTagsPath + booking_code + \
        '/' + os.path.basename(securedFileName)

    if os.path.exists(nameTagFilename) and os.path.isfile(nameTagFilename):
        os.remove(nameTagFilename)
        return FilePath(filename=nameTagFilename)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="NameTag not found")
