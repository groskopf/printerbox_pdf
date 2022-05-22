from reportlab.lib.units import mm

from pdf.doc_templates import NameTag4786103DocTemplate
from name_data import NameData
from pdf.layouts import Layout, NameTagLayout1Table, ReversedNameTagLayout1Table


def create(fileName : str, layout: Layout, nameData: NameData):
    doc = NameTag4786103DocTemplate(fileName)

    story = []

    if(layout == Layout.LAYOUT_1):
        story.append(NameTagLayout1Table(103*mm, 70*mm, nameData))
        story.append(ReversedNameTagLayout1Table(103*mm, 70*mm, nameData))

    doc.build(story)
