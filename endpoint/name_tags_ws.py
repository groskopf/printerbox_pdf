import os
from typing import List
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from file_path import FilePath
from site_paths import nameTagsPath
from printer_code import PrinterCode

router = APIRouter()


class WSConnection():
    websocket: WebSocket
    booking_code: str

    def __init__(self, webSocket: WebSocket, booking_code: str):
        self.websocket = webSocket
        self.booking_code = booking_code


class WSConnectionManager:
    def __init__(self):
        self.connections: List[WSConnection] = []

    async def connect(self, connection: WSConnection):
        await connection.websocket.accept()
        print("New connection: " + connection.booking_code)
        self.connections.append(connection)

    def disconnect(self, connection: WSConnection):
        self.connections.remove(connection)

    async def sendToPrinter(self, booking_code: str, message: str):
        for connection in self.connections:
            if connection.booking_code == booking_code:
                print("Sending to: " + connection.booking_code + " : " + message)
                await connection.websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.websocket.send_text(message)


def deleteFilesInPrinterQueue(booking_code: str):
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(nameTagsPath + booking_code, topdown=False):
        for name in foundFiles:
            filename = os.path.join(root, name)
            files.append(FilePath(filename=filename))
            os.remove(filename)

    return files


def getFilesInPrinterQueue(booking_code: str):
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(nameTagsPath + booking_code, topdown=False):
        for name in foundFiles:
            files.append(FilePath(filename=os.path.join(root, name)))

    return files


wsConnectionManager = WSConnectionManager()


@router.websocket("/{booking_code}/ws")
async def websocket_endpoint(websocket: WebSocket, booking_code: str):
    connection = WSConnection(websocket, booking_code)
    await wsConnectionManager.connect(connection)

    try:
        for filename in getFilesInPrinterQueue(booking_code):
            await wsConnectionManager.sendToPrinter(connection.booking_code, filename.json())

        while True:
            # Just reply what is received
            data = await websocket.receive_text()
            await wsConnectionManager.sendToPrinter(connection.booking_code, data)
    except WebSocketDisconnect:
        wsConnectionManager.disconnect(connection)
