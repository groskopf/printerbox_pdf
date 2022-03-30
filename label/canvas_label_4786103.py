from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class CanvasLabel4786103(canvas.Canvas):

    pageWidth=76*mm
    pageHight=103*mm
    pageSize = (pageWidth, pageHight)
    
    def __init__(self, name):
        Canvas.__init__(name, pageSize)