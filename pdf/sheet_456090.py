from reportlab.lib.units import mm
from typing import List

from pdf.doc_templates import Sheet456090DocTemplate
from name_data import NameData
from pdf.layouts import Layout, NameTagLayout3BaseTable, SheetTable

labelWidth = 90*mm
labelHeight = 60*mm


def create(fileName, layout: Layout, nameDataList: List[NameData]):
    labels = []

    if(layout == Layout.LAYOUT_1):
        for nameData in nameDataList:
            labels.append(NameTagLayout3BaseTable(labelWidth,
                                              labelHeight,
                                              nameData))

        colounms = 2

    doc = Sheet456090DocTemplate(fileName)

    story = []
    story.append(SheetTable(colounms, labelWidth, labelHeight, labels))

    doc.build(story)
