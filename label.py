from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet


nameField = '<para alignment="center"> Paul Groskopf</para>'
# nameField = '<para alignment="center">' + 'Paul Groskopf'

pageWidth=76*mm
pageHight=103*mm
pageTop = pageHight


pageSize = (pageWidth, pageHight)

c = canvas.Canvas("label.pdf", pageSize, bottomup = 1)

frameWidth = pageWidth - 20*mm
frameHight = 10*mm
frame1 = Frame(10*mm, pageTop - 10*mm - frameHight, frameWidth, frameHight, showBoundary=1)

styles = getSampleStyleSheet()
normal = styles['Normal']
nameParagraph = [Paragraph(nameField, normal)]
nameFrame = KeepInFrame(frameWidth, frameHight, nameParagraph)
frame1.addFromList([nameFrame], c)

c.drawCentredString(pageWidth/2, 10 * mm, "Paul Groskopf")
c.line(20 * mm, 3 * mm, pageWidth - 20 * mm, 3 * mm)
c.save()
