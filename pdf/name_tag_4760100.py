from reportlab.lib.units import mm

from pdf.doc_templates import NameTag4760100DocTemplate
from name_data import NameData
from pdf.layouts import Layout, createNameTag


def create(fileName: str, layout: Layout, nameData: NameData):

    leftPadding = 2*mm
    rightPadding = 2*mm
    topPadding = 2*mm
    bottomPadding = 2*mm

    height = 60*mm - topPadding - bottomPadding
    width = 100*mm - leftPadding - rightPadding

    doc = NameTag4760100DocTemplate(fileName)

    story = []

    front = createNameTag(layout, width=width, height=height, nameData=nameData)
    story.append(front)                           

    doc.build(story)
