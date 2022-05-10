
'''
Created on 31. mar. 2022

@author: paul
'''
from reportlab.lib.units import mm
from typing import List

from pdf.DocTemplates import NameTagSheet456090DocTemplate
from pdf.Layouts import NameData
from pdf.Layouts import NameTagLayout1Table
from pdf.Layouts import NameTagSheetTable

labelWidth=90*mm
labelHeight=60*mm

def createNameTagSheet456090(fileName, layout : str, nameDataList: List[NameData]):
        labels = []
        
        if(layout == "layout_1"):
            for nameData in nameDataList:
                labels.append(NameTagLayout1Table(labelWidth,
                                                  labelHeight,
                                                  nameData))
        
            colounms = 2
        
        doc = NameTagSheet456090DocTemplate(fileName)
        
        story = []
        story.append(NameTagSheetTable(colounms, labelWidth, labelHeight, labels))
        
        doc.build(story)

