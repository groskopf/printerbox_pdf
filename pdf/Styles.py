
'''
Created on 31. mar. 2022

@author: paul
'''
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


# to kolonner med 5 rækker 60x90
styleSheet = getSampleStyleSheet()
normalCenterStyle = styleSheet["Normal"]
normalCenterStyle.alignment = TA_CENTER
normalCenterStyle.splitLongWords = 1
normalCenterStyle.wordWrap = 1

heading1CenterStyle = styleSheet["Heading1"]
heading1CenterStyle.alignment = TA_CENTER
heading1CenterStyle.splitLongWords = 1

