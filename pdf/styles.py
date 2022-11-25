from reportlab.lib.styles import getSampleStyleSheet, _baseFontNameB
from reportlab.lib.enums import TA_CENTER

styleSheet = getSampleStyleSheet()

nameStyle = styleSheet["Normal"]
nameStyle.alignment = TA_CENTER
nameStyle.fontSize = 18
nameStyle.spaceBefore=10
nameStyle.splitLongWords = 1

titleStyle = styleSheet["Normal"]
titleStyle.alignment = TA_CENTER
titleStyle.fontSize = 14
titleStyle.spaceBefore=10
titleStyle.spaceAfter=10
titleStyle.splitLongWords = 1

companyStyle = styleSheet["Normal"]
companyStyle.alignment = TA_CENTER
companyStyle.fontName = _baseFontNameB
companyStyle.fontSize = 16
companyStyle.spaceBefore=10
companyStyle.splitLongWords = 1

smallCompanyStyle = styleSheet["Italic"]
smallCompanyStyle.alignment = TA_CENTER
smallCompanyStyle.fontSize = 12
smallCompanyStyle.spaceBefore=6
smallCompanyStyle.splitLongWords = 1
