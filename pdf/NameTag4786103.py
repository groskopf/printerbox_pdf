
'''
Created on 31. mar. 2022

@author: paul
'''

from reportlab.lib.units import mm

from pdf.DocTemplates import NameTag4786103DocTemplate
from pdf.Layouts import NameData 
from pdf.Layouts import NameTagLayout1Table, ReversedNameTagLayout1Table

def createNameTag4786103(fileName, layout, nameData):
    doc = NameTag4786103DocTemplate(fileName)

    story = []

    if(layout == "layout_1"):
        story.append(NameTagLayout1Table(103*mm, 70*mm, nameData))
        story.append(ReversedNameTagLayout1Table(103*mm, 70*mm, nameData))

    doc.build(story)

