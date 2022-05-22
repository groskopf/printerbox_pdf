import os
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from filePaths import queuesPath
from printer_code import PrinterCode


class Filename(BaseModel):
    filename : str

class WSConnection():
    websocket : WebSocket
    printerCode : PrinterCode

    def __init__(self, webSocket : WebSocket, printerCode : PrinterCode):
        self.websocket = webSocket
        self.printerCode = printerCode


class WSConnectionManager:
    def __init__(self):
        self.connections: List[WSConnection] = []

    async def connect(self, connection : WSConnection):
        await connection.websocket.accept()
        self.connections.append(connection)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def sendToPrinter(self, printerCode : PrinterCode, message: str):
        for connection in self.connections:
            if connection.printerCode == printerCode:
                await connection.websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.websocket.send_text(message)


def allFilesInPrinterQueue(printerCode : PrinterCode):
    files : List[Filename] = []
    
    for root, dirs, foundFiles in os.walk(queuesPath + printerCode, topdown=False):
        for name in foundFiles:
            files.append(Filename(filename=os.path.join(root, name)))
    
    return files



router = APIRouter()
wsConnectionManager = WSConnectionManager()


@router.get('/{printer_code}')
def printerboxQueue(printer_code : PrinterCode):
    return allFilesInPrinterQueue(printer_code)

@router.websocket("/ws/{printer_code}")
async def websocket_endpoint(websocket: WebSocket, printer_code: PrinterCode):
    connection = WSConnection(websocket, printer_code)
    await wsConnectionManager.connect(connection)

    for filename in allFilesInPrinterQueue(printer_code):
        await wsConnectionManager.sendToPrinter(connection.printerCode, filename.json())

    try:
        while True:
            # Just reply what is received
            data =await websocket.receive_text()
            await wsConnectionManager.sendToPrinter(connection.printerCode, data)
    except WebSocketDisconnect:
        wsConnectionManager.disconnect(websocket)