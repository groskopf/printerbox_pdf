from reportlab.lib.units import mm
from typing import List

from pdf.doc_templates import NameTagSheet456090DocTemplate
from name_data import NameData
from pdf.layouts import Layout, NameTagLayout1Table, NameTagSheetTable

labelWidth = 90*mm
labelHeight = 60*mm


def create(fileName, layout: Layout, nameDataList: List[NameData]):
    labels = []

    if(layout == Layout.LAYOUT_1):
        for nameData in nameDataList:
            labels.append(NameTagLayout1Table(labelWidth,
                                              labelHeight,
                                              nameData))

        colounms = 2

    doc = NameTagSheet456090DocTemplate(fileName)

    story = []
    story.append(NameTagSheetTable(colounms, labelWidth, labelHeight, labels))

    doc.build(story)
