from reportlab.lib.units import mm

from pdf.doc_templates import NameTag4786103DocTemplate
from name_data import NameData
from pdf.layouts import Layout, createNameTag


def create(fileName: str, layout: Layout, nameData: NameData):

    leftPadding = 3*mm
    rightPadding = 3*mm
    topPadding = 16*mm
    bottomPadding = 16*mm

    height = 86*mm - topPadding
    width = 103*mm - leftPadding - rightPadding

    doc = NameTag4786103DocTemplate(fileName)

    story = []

    front = createNameTag(layout, width=width, height=height, nameData=nameData)
    back = createNameTag(layout, width=width, height=height, nameData=nameData)
    back.upsideDown=True
    story.append(front)                           
    story.append(back)                           

    doc.build(story)
