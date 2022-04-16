
'''
Created on 31. mar. 2022

@author: paul
'''
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, PageTemplate, Frame, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import _doNothing
from reportlab.platypus.para import FastPara, Paragraph
from reportlab.platypus.flowables import KeepInFrame, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

PAGE_HEIGHT = 210 * mm
PAGE_WIDTH = 297 * mm
LABEL_HEIGHT = 60 * mm
LABEL_WIDTH = 90 * mm
LEFT_MARGIN = ((PAGE_WIDTH - LABEL_WIDTH * 2) / 2)

styleSheet = getSampleStyleSheet()

Title = "476090 ark"
pageinfo = "Navnelabel ark 60x90"

# to kolonner med 5 rækker 60x90

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(0, 0, PAGE_HEIGHT, PAGE_WIDTH,topPadding=0, id='WHOLE_PAGE', showBoundary=0)])
        self.addPageTemplates(template)

doc = MyDocTemplate("label_ark_xx6090.pdf") 

def makeLabel(topFieldText, middleFieldText, bottomFieldText):
    normalCenterStyle = styleSheet["Normal"]
    normalCenterStyle.alignment = TA_CENTER
    normalCenterStyle.splitLongWords = 1 
    normalCenterStyle.wordWrap = 1 
    
    headingCenterStyle = styleSheet["Heading1"]
    headingCenterStyle.alignment = TA_CENTER
    headingCenterStyle.splitLongWords = 1 
   
    fieldWidth = LABEL_WIDTH
    topFieldHeight = LABEL_HEIGHT/4 
    middleFieldHeight = LABEL_HEIGHT/4
    bottomFieldHeight = LABEL_HEIGHT/2 
    
    topFieldParagraph = Paragraph(topFieldText, normalCenterStyle)
    middleFieldParagraph = Paragraph(middleFieldText, headingCenterStyle)
    bottomFieldParagraph = Paragraph(bottomFieldText, normalCenterStyle)
    bottomFieldImage = Image('Kongresartikler.jpg', width=bottomFieldHeight, height=bottomFieldHeight)
    bottomFieldImage.hAlign = 'LEFT'
    bottomFieldTable = Table([[bottomFieldImage, bottomFieldParagraph]],
                       [bottomFieldHeight, fieldWidth-bottomFieldHeight], 
                       [bottomFieldHeight])
    
    bottomFieldTableStyle = TableStyle()
    bottomFieldTableStyle.add('VALIGN', (0, 0), (-1, -1), 'RIGHT')
    bottomFieldTableStyle.add('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
    bottomFieldTableStyle.add('BOX', (0, 0), (-1, -1), 1, colors.black)
    bottomFieldTable.setStyle(bottomFieldTableStyle)
    
    allFieldParagraphs = [[KeepInFrame(fieldWidth, topFieldHeight, [topFieldParagraph])], 
                          [KeepInFrame(fieldWidth, middleFieldHeight, [middleFieldParagraph])], 
                          [KeepInFrame(fieldWidth, bottomFieldHeight, [bottomFieldTable])]] 
    
    labelTable = Table(allFieldParagraphs, 
                       [fieldWidth], 
                       [topFieldHeight, middleFieldHeight, bottomFieldHeight],
                       spaceBefore=0, spaceAfter=0)
    labelStyle = TableStyle()
    labelStyle.add('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    labelStyle.add('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
    labelStyle.add('BOX', (0, 0), (-1, -1), 1, colors.black)
    labelTable.setStyle(labelStyle)
    
    return labelTable

navneListe = [
                ['H. P. Valdal A/S', 'Hans Peter Valdal', 'Direktør'],
                ['Groskopf Embedded', 'Paul Friedrich Groskopf', 'Selvstændig'],
                ['Kongresartikler.dk', 'Inge-Lise Valdal', 'Bogholderi og lagerchef'],
                ['Stormcut.dk', 'Anne Dorthe Valdal Groskopf', 'Salg og marketing'],
                ['Valdal Advokatfirma', 'Kresten Valdal', 'Advokat'],
                ]

labels = []

for navn in navneListe:
    labels.append(makeLabel(navn[0], navn[1], navn[2]))

colounms = 2

# Fill up with empty labels
emptyLabelsInLastRow = len(labels) % colounms
if (emptyLabelsInLastRow > 0):
    labels.append(5 * '')
    
rows = int(len(labels)/colounms)

labelTableData = [ labels[i:i+colounms] for i in range(0, len(labels), colounms) ]

t = Table(labelTableData, colWidths=(colounms * [LABEL_WIDTH]), rowHeights=(rows * [LABEL_HEIGHT]), spaceBefore=0, spaceAfter=0)
tableStyle = TableStyle()
tableStyle.add('ALIGN', (-1, -1), (-1,-1), 'RIGHT')
tableStyle.add('VALIGN', (-1, -1), (-1, -1), 'MIDDLE')
tableStyle.add('INNERGRID', (0, 0), (-1, -1), 1, colors.black)
tableStyle.add('BOX', (0, 0), (-1, -1), 1, colors.black)
tableStyle.add('TOPPADDING', (0, 0), (-1, -1), 1)
tableStyle.add('BOTTOMPADDING', (0, 0), (-1, -1), 1)
tableStyle.add('LEFTPADDING', (0, 0), (-1, -1), 1)
tableStyle.add('RIGHTPADDING', (0, 0), (-1, -1), 1)
t.setStyle(tableStyle)

# t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
story = []
story.append(t)
doc.build(story)
