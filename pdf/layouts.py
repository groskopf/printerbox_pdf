from enum import Enum, Flag
from reportlab.platypus import Table, TableStyle
from reportlab.platypus.para import Paragraph
from reportlab.platypus.flowables import KeepInFrame, Image
from reportlab.lib import colors
from reportlab_qrcode import QRCodeImage

from endpoint.config import config
from name_data import NameData
from pdf.styles import nameStyle, titleStyle, companyStyle, smallCompanyStyle


gridColor: bool = colors.white
if config.show_frames:
    gridColor = colors.black


class Justify(Flag):
    Left = True
    Right = False


class Layout(str, Enum):
    LAYOUT_1 = "layout_1"
    LAYOUT_2 = "layout_2"
    LAYOUT_2PT = "layout_2PT"
    LAYOUT_2PB = "layout_2PB"
    LAYOUT_2PTL = "layout_2PTL"
    LAYOUT_2PTR = "layout_2PTR"
    LAYOUT_2PBL = "layout_2PBL"
    LAYOUT_2PBR = "layout_2PBR"
    LAYOUT_3 = "layout_3"
    LAYOUT_3PT = "layout_3PT"
    LAYOUT_3PB = "layout_3PB"
    LAYOUT_3PTL = "layout_3PTL"
    LAYOUT_3PTR = "layout_3PTR"
    LAYOUT_3PBL = "layout_3PBL"
    LAYOUT_3PBR = "layout_3PBR"
    LAYOUT_INVALID = "invalid"


class NoPaddingTableStyle(TableStyle):
    def __init__(self, cmds=None, parent=None,
                 valign: str = None,
                 align: str = None,
                 **kw):
        super().__init__(cmds, parent, **kw)

        self.add('INNERGRID', (0, 0), (-1, -1), 1, gridColor)
        self.add('BOX', (0, 0), (-1, -1), 1, gridColor)

        self.add('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        if valign:
            self.add(valign[0], valign[1], valign[2], valign[3])

        if align:
            self.add('ALIGN', (0, 0), (-1, -1), align)
        else:
            self.add('ALIGN', (0, 0), (-1, -1), 'CENTER')

        self.add('TOPPADDING', (0, 0), (-1, -1), 0)
        self.add('BOTTOMPADDING', (0, 0), (-1, -1), 0)
        self.add('LEFTPADDING', (0, 0), (-1, -1), 0)
        self.add('RIGHTPADDING', (0, 0), (-1, -1), 0)


class UpsideDownTable(Table):
    upsideDown = False
    valign = None

    def __init__(self, *args, **kwargs):
        Table.__init__(self, *args, **kwargs)
        self.setStyle(NoPaddingTableStyle(valign=self.valign))

    def draw(self):
        if self.upsideDown:
            c = self.canv
            c.rotate(180)
            c.translate(-self._width, -self._height)

        Table.draw(self)


class ImageAndParagraphTable(Table):
    def __init__(self, width, height, text, nameData: NameData, justify: Justify):
        imageName = nameData.image_name
        qrCode = nameData.qr_code
        if imageName and len(imageName):
            image = Image('images/' + imageName)
            image._restrictSize(height, height)
        elif qrCode and len(qrCode):
            image = QRCodeImage(qrCode, height)
        else:
            image = ""

        paragraph = Paragraph(text, companyStyle)

        if justify == Justify.Left:
            cellContent = [[image, paragraph]]
            cellWidths = [height, width - height]
        else:
            cellContent = [[paragraph, image]]
            cellWidths = [width - height, height]

        # Image is squared and the rest of the width is for text paragraph
        cellHeights = [height]

        Table.__init__(self, cellContent, cellWidths, cellHeights)

        self.setStyle(NoPaddingTableStyle())


class NameTagLayout1Table(UpsideDownTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height]

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_3, companyStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])

        linesContent = [[KeepInFrame(width, lineHeights[0], lines[0])]]

        lineWidths = [width]

        UpsideDownTable.__init__(self, linesContent, lineWidths, lineHeights)


class NameTagLayout2BaseTable(UpsideDownTable):
    def __init__(self, width, lineHeights, lines):
        linesContent = [[KeepInFrame(width, lineHeights[0], lines[0])],
                        [KeepInFrame(width, lineHeights[1], lines[1])]]

        lineWidths = [width]

        UpsideDownTable.__init__(self, linesContent, lineWidths, lineHeights)

    def wrap(self, availWidth, availHeight):
        return Table.wrap(self, availWidth, availHeight)


class NameTagLayout2Table(NameTagLayout2BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(2/3), height*(1/3)]

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])

        self.valign = ['VALIGN', (0, -1), (0, -1), 'TOP']

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout2PTTable(UpsideDownTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height/2, height/2]

        image = Image('images/' + nameData.image_name)
        image._restrictSize(width, lineHeights[0])

        lines = []
        lines.append([image])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_3, companyStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout2PBTable(UpsideDownTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height/2, height/2]

        image = Image('images/' + nameData.image_name)
        image._restrictSize(width, lineHeights[1])

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_3, companyStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([image])

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3BaseTable(UpsideDownTable):
    def __init__(self, width, lineHeights, lines):
        linesContent = [[KeepInFrame(width, lineHeights[0], lines[0])],
                        [KeepInFrame(width, lineHeights[1], lines[1])],
                        [KeepInFrame(width, lineHeights[2], lines[2])]]

        lineWidths = [width]

        UpsideDownTable.__init__(self, linesContent, lineWidths, lineHeights)

    def wrap(self, availWidth, availHeight):
        return Table.wrap(self, availWidth, availHeight)


class NameTagLayout2PBLTable(NameTagLayout2BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(2/3), height*(1/3)]

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([ImageAndParagraphTable(width, lineHeights[1],
                                             nameData.line_3, nameData,
                                             Justify.Left)])

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout2PBRTable(NameTagLayout2BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(2/3), height*(1/3)]

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([ImageAndParagraphTable(width, lineHeights[1],
                                             nameData.line_3, nameData,
                                             Justify.Right)])

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout2PTLTable(NameTagLayout2BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(1/3), height*(2/3)]

        lines = []
        lines.append([ImageAndParagraphTable(width, lineHeights[0],
                                             nameData.line_3, nameData,
                                             Justify.Left)])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                     Paragraph(nameData.line_2, titleStyle)])

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout2PTRTable(NameTagLayout2BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(1/3), height*(2/3)]

        lines = []
        lines.append([ImageAndParagraphTable(width, lineHeights[0],
                                             nameData.line_3, nameData,
                                             Justify.Right)])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])

        NameTagLayout2BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3Table(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(1/4), height*(2/4), height*(1/4)]

        lines = []
        lines.append([Paragraph(nameData.line_3, companyStyle)])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_4, companyStyle)])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3PTTable(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(1/4), height*(2/4), height*(1/4)]

        image = Image('images/' + nameData.image_name)
        image._restrictSize(width, lineHeights[2])

        lines = []
        lines.append([image])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3PBTable(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(2/4), height*(1/4), height*(1/4)]

        image = Image('images/' + nameData.image_name)
        image._restrictSize(width, lineHeights[0])

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_4, smallCompanyStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])
        lines.append([image])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3PTLTable(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(1/4), height*(2/4), height*(1/4)]

        lines = []
        lines.append([ImageAndParagraphTable(width, lineHeights[2],
                                             nameData.line_4, nameData,
                                             Justify.Left)])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3PTRTable(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(1/4), height*(2/4), height*(1/4)]

        lines = []
        lines.append([ImageAndParagraphTable(width, lineHeights[2],
                                             nameData.line_4, nameData,
                                             Justify.Right)])
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3PBLTable(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(2/4), height*(1/4), height*(1/4)]

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])
        lines.append([ImageAndParagraphTable(width, lineHeights[2],
                                             nameData.line_4, nameData,
                                             Justify.Left)])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


class NameTagLayout3PBRTable(NameTagLayout3BaseTable):
    def __init__(self, width: float, height: float, nameData: NameData):

        lineHeights = [height*(2/4), height*(1/4), height*(1/4)]

        lines = []
        lines.append([Paragraph(nameData.line_1, nameStyle),
                      Paragraph(nameData.line_2, titleStyle),
                      Paragraph(nameData.line_5, smallCompanyStyle)
                      ])
        lines.append([Paragraph(nameData.line_3, companyStyle)])
        lines.append([ImageAndParagraphTable(width, lineHeights[2],
                                             nameData.line_4, nameData,
                                             Justify.Right)])

        NameTagLayout3BaseTable.__init__(self, width, lineHeights, lines)


def createNameTag(layout: Layout, width: float, height: float, nameData: NameData):
    match layout:
        case Layout.LAYOUT_1:
            return NameTagLayout1Table(width, height, nameData)
        case Layout.LAYOUT_2:
            return NameTagLayout2Table(width, height, nameData)
        case Layout.LAYOUT_2PT:
            return NameTagLayout2PTTable(width, height, nameData)
        case Layout.LAYOUT_2PB:
            return NameTagLayout2PBTable(width, height, nameData)
        case Layout.LAYOUT_2:
            return NameTagLayout2Table(width, height, nameData)
        case Layout.LAYOUT_2PT:
            return NameTagLayout2PTTable(width, height, nameData)
        case Layout.LAYOUT_2PB:
            return NameTagLayout2PBTable(width, height, nameData)
        case Layout.LAYOUT_2PTL:
            return NameTagLayout2PTLTable(width, height, nameData)
        case Layout.LAYOUT_2PTR:
            return NameTagLayout2PTRTable(width, height, nameData)
        case Layout.LAYOUT_2PBL:
            return NameTagLayout2PBLTable(width, height, nameData)
        case Layout.LAYOUT_2PBR:
            return NameTagLayout2PBRTable(width, height, nameData)
        case Layout.LAYOUT_3:
            return NameTagLayout3Table(width, height, nameData)
        case Layout.LAYOUT_3PT:
            return NameTagLayout3PTTable(width, height, nameData)
        case Layout.LAYOUT_3PB:
            return NameTagLayout3PBTable(width, height, nameData)
        case Layout.LAYOUT_3PTR:
            return NameTagLayout3PTRTable(width, height, nameData)
        case Layout.LAYOUT_3PTL:
            return NameTagLayout3PTLTable(width, height, nameData)
        case Layout.LAYOUT_3PBR:
            return NameTagLayout3PBRTable(width, height, nameData)
        case Layout.LAYOUT_3PBL:
            return NameTagLayout3PBLTable(width, height, nameData)


class SheetTable(Table):
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

        self.setStyle(NoPaddingTableStyle())
