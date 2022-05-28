import os
from typing import List
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from file_path import FilePath
from site_paths import printersPath
from printer_code import PrinterCode

router = APIRouter()



class WSConnection():
    websocket: WebSocket
    printerCode: PrinterCode

    def __init__(self, webSocket: WebSocket, printerCode: PrinterCode):
        self.websocket = webSocket
        self.printerCode = printerCode


class WSConnectionManager:
    def __init__(self):
        self.connections: List[WSConnection] = []

    async def connect(self, connection: WSConnection):
        await connection.websocket.accept()
        self.connections.append(connection)

    def disconnect(self, connection: WSConnection):
        self.connections.remove(connection)

    async def sendToPrinter(self, printerCode: PrinterCode, message: str):
        for connection in self.connections:
            if connection.printerCode == printerCode:
                await connection.websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.websocket.send_text(message)


def allFilesInPrinterQueue(printerCode: PrinterCode):
    files: List[FilePath] = []

    for root, dirs, foundFiles in os.walk(printersPath + printerCode, topdown=False):
        for name in foundFiles:
            files.append(FilePath(filename=os.path.join(root, name)))

    return files


wsConnectionManager = WSConnectionManager()


@router.websocket("/{printer_code}/ws")
async def websocket_endpoint(websocket: WebSocket, printer_code: PrinterCode):
    connection = WSConnection(websocket, printer_code)
    await wsConnectionManager.connect(connection)

    try:
        for filename in allFilesInPrinterQueue(printer_code):
            await wsConnectionManager.sendToPrinter(connection.printerCode, filename.json())

        while True:
            # Just reply what is received
            data = await websocket.receive_text()
            await wsConnectionManager.sendToPrinter(connection.printerCode, data)
    except WebSocketDisconnect:
        wsConnectionManager.disconnect(connection)
