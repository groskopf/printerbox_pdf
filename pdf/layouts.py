from enum import Enum
from reportlab.platypus import Table, TableStyle
from reportlab.platypus.para import Paragraph
from reportlab.platypus.flowables import KeepInFrame, Image
from reportlab.lib import colors

from endpoint.name_data import NameData
from pdf.styles import normalCenterStyle, heading1CenterStyle


class Layout(str, Enum):
    LAYOUT_1 = "layout_1"
    LAYOUT_2 = "layout_2"


class LeftImageAndParagraphTable(Table):
    def __init__(self, width, height, text, imageName):
        image = Image('images/' + imageName)
        # FIXME what if width is larger then height
        image._restrictSize(height, height)
        image.hAlign = 'LEFT'  # FIXME is this needed ???

        paragraph = Paragraph(text, normalCenterStyle)
        cellContent = [[image, paragraph]]

        # Image is squared and the rest of the width is for text paragraph
        cellWidths = [height, width - height]
        cellHeights = [height]

        Table.__init__(self, cellContent, cellWidths, cellHeights)

        style = TableStyle()
        style.add('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        style.add('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
        style.add('BOX', (0, 0), (-1, -1), 1, colors.black)
        style.add('TOPPADDING', (0, 0), (-1, -1), 0)
        style.add('TOPPADDING', (0, 0), (-1, -1), 0)
        style.add('BOTTOMPADDING', (0, 0), (-1, -1), 0)
        self.setStyle(style)


class NameTagLayout1Table(Table):
    def __init__(self, width, height, nameData: NameData):
        cellWidth = width
        topCellHeight = height / 4
        middleCellHeight = height / 4
        bottomCellHeight = height / 2

        topCell = [Paragraph(nameData.description1, normalCenterStyle)]
        middleCell = [Paragraph(nameData.name, heading1CenterStyle)]
        bottomCell = [LeftImageAndParagraphTable(
            cellWidth, bottomCellHeight, nameData.description2, nameData.imageName)]

        allCellsContent = [[KeepInFrame(cellWidth, topCellHeight, topCell)],
                           [KeepInFrame(
                               cellWidth, middleCellHeight, middleCell)],
                           [KeepInFrame(cellWidth, bottomCellHeight, bottomCell)]]

        cellWidths = [cellWidth]
        cellHeights = [topCellHeight, middleCellHeight, bottomCellHeight]

        Table.__init__(self, allCellsContent, cellWidths, cellHeights)

        style = TableStyle()
        style.add('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        style.add('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
        style.add('BOX', (0, 0), (-1, -1), 1, colors.black)
        style.add('TOPPADDING', (0, 0), (-1, -1), 0)
        style.add('BOTTOMPADDING', (0, 0), (-1, -1), 0)
        style.add('LEFTPADDING', (0, 0), (-1, -1), 0)
        style.add('RIGHTPADDING', (0, 0), (-1, -1), 0)
        self.setStyle(style)

    def wrap(self, availWidth, availHeight):
        return Table.wrap(self, availWidth, availHeight)

    def draw(self):
        Table.draw(self)


class ReversedNameTagLayout1Table(NameTagLayout1Table):
    def __init__(self, *args):
        NameTagLayout1Table.__init__(self, *args)

    def draw(self):
        c = self.canv
        c.rotate(180)
        c.translate(-self._width, -self._height)

        Table.draw(self)


class NameTagSheetTable(Table):
    def __init__(self, colounms, labelWidth, labelHeight, labels):
        # Fill up with empty labels
        emptyLabelsInLastRow = len(labels) % colounms
        if (emptyLabelsInLastRow > 0):
            for _ in range(emptyLabelsInLastRow):
                labels.append('')

        rows = int(len(labels)/colounms)

        # Reformat to 2D array
        labelTableData = [labels[i:i+colounms]
                          for i in range(0, len(labels), colounms)]

        Table.__init__(self, labelTableData, colWidths=(
            colounms * [labelWidth]), rowHeights=(rows * [labelHeight]), spaceBefore=0, spaceAfter=0)

        tableStyle = TableStyle()
        tableStyle.add('ALIGN', (-1, -1), (-1, -1), 'RIGHT')
        tableStyle.add('VALIGN', (-1, -1), (-1, -1), 'MIDDLE')
        tableStyle.add('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
        tableStyle.add('BOX', (0, 0), (-1, -1), 1, colors.black)
        tableStyle.add('TOPPADDING', (0, 0), (-1, -1), 0)
        tableStyle.add('BOTTOMPADDING', (0, 0), (-1, -1), 0)
        tableStyle.add('LEFTPADDING', (0, 0), (-1, -1), 0)
        tableStyle.add('RIGHTPADDING', (0, 0), (-1, -1), 0)
        self.setStyle(tableStyle)
