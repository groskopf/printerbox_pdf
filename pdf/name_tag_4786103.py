from reportlab.lib.units import mm
from reportlab.platypus import Table
from reportlab.platypus.para import Paragraph
from reportlab.platypus.flowables import KeepInFrame
from pdf.doc_templates import NameTag4786103DocTemplate
from pdf.layouts import Layout, NoPaddingTableStyle, createNameTag
from name_data import NameData

class Spacer(Table):
    def __init__(self, width: float, height: float):
        # Create a 1x1 table with an empty string as the only cell
        linesContent = [[""]]
        lineWidths = [width]
        lineHeights = [height]
        Table.__init__(self, linesContent, lineWidths, lineHeights)
        #self.setStyle(NoPaddingTableStyle(valign=self.valign))


def create(
    fileName: str,
    layout: Layout,
    nameData: NameData,
    single_page: bool = False,
):
    leftPadding = 3*mm
    rightPadding = 3*mm
    topPadding = 16*mm
    bottomPadding = 2*mm

    height = 86*mm - topPadding - bottomPadding
    width = 103*mm - leftPadding - rightPadding

    doc = NameTag4786103DocTemplate(fileName, single_page=single_page)

    story = []

    front = createNameTag(
        layout,
        width=width,
        height=height,
        nameData=nameData,
    )
    story.append(front)
    story.append(Spacer(width, bottomPadding))
    
    if not single_page:
        story.append(Spacer(width, bottomPadding))
        back = createNameTag(
            layout,
            width=width,
            height=height,
            nameData=nameData,
        )
        back.upsideDown = True
        story.append(back)

    doc.build(story)
