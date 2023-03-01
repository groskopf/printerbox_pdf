from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, _baseFontNameB
from reportlab.lib.enums import TA_CENTER


styleSheet = getSampleStyleSheet()


nameStyle = ParagraphStyle(name='NameStyle',
                           parent=styleSheet['Normal'],
                           alignment=TA_CENTER,
                           fontSize=18,
                           fontName=_baseFontNameB,
                           spaceBefore=10,
                           splitLongWords=1,
                           leading=20
                           )

titleStyle = ParagraphStyle(name='TitleStyle',
                            parent=styleSheet['Normal'],
                            alignment=TA_CENTER,
                            fontSize=14,
                            spaceBefore=10,
                            spaceAfter=10,
                            splitLongWords=1,
                            leading=16
                            )

companyStyle = ParagraphStyle(name='CompanyStyle',
                              parent=styleSheet['Normal'],
                              alignment=TA_CENTER,
                              fontSize=16,
                              fontName=_baseFontNameB,
                              spaceBefore=10,
                              splitLongWords=1,
                              leading=18
                              )

smallCompanyStyle = ParagraphStyle(name='SmallCompanyStyle',
                                   parent=styleSheet['Italic'],
                                   alignment=TA_CENTER,
                                   fontSize=12,
                                   spaceBefore=6,
                                   splitLongWords=1,
                                   leading=14
                                   )
