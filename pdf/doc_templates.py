from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4


class NameTagDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename,
                                 author='kongresartikler.dk',
                                 creator='kongresartikler.dk',
                                 producer='kongresartikler.dk',
                                 **kwargs)


class NameTag4760100DocTemplate(NameTagDocTemplate):
    def __init__(self, filename):
        pageWidth = 104*mm
        pageHeight = 60*mm
        NameTagDocTemplate.__init__(self, filename,
                                    pagesize=(pageWidth, pageHeight),
                                    title='Navneskilt 4760100',
                                    subject="Label navneskilt 60x100mm")
        pageFrame = Frame(0, 0, pageWidth, pageHeight,
                          topPadding=3 * mm,
                          bottomPadding=3 * mm
                          )
        template = PageTemplate('normal', [pageFrame])
        self.addPageTemplates(template)



class NameTag4786103DocTemplate(NameTagDocTemplate):
    def __init__(self, filename):
        pageWidth = 103*mm
        pageHeight = 172*mm
        NameTagDocTemplate.__init__(self, filename,
                                    pagesize=(pageWidth, pageHeight),
                                    title='Navneskilt 4786103',
                                    subject="Foldbart navneskilt 86x103mm")
        pageFrame = Frame(0, 0, pageWidth, pageHeight,
                          topPadding=16 * mm,
                          bottomPadding=16 * mm
                          )
        template = PageTemplate('normal', [pageFrame])
        self.addPageTemplates(template)


class Sheet456090DocTemplate(NameTagDocTemplate):
    def __init__(self, filename):
        pageWidth, pageHeight = A4
        NameTagDocTemplate.__init__(self, filename,
                                    pagesize=A4,
                                    title='Navneskilte 456090',
                                    subject="Foldbart navneskilt 86x103mm")
        pageFrame = Frame(0, 0, pageWidth, pageHeight,
                          topPadding=0, bottomPadding=0)
        template = PageTemplate('normal', [pageFrame])
        self.addPageTemplates(template)
