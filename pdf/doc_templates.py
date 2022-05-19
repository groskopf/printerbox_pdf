from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4


class NameTagDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename,
                                 author='printerbox.dk',
                                 creator='printerbox.dk',
                                 producer='printerbox.dk',
                                 **kwargs)


class NameTag4786103DocTemplate(NameTagDocTemplate):
    def __init__(self, filename):
        pageWidth = 103*mm
        pageHeight = 172*mm
        NameTagDocTemplate.__init__(self, filename,
                                    pagesize=(pageWidth, pageHeight),
                                    title='Navneskilt 4786103',
                                    subject="Foldbart navneskilt 86x103mm")
        pageFrame = Frame(0, 0, pageWidth, pageHeight,
                          topPadding=16 * mm, bottomPadding=16 * mm)
        template = PageTemplate('normal', [pageFrame])
        self.addPageTemplates(template)


class NameTagSheet456090DocTemplate(NameTagDocTemplate):
    def __init__(self, filename):
        pageWidth, pageHeight = A4
        NameTagDocTemplate.__init__(self, filename,
                                    pagesize=A4,
                                    title='Navneskilte ' + filename,
                                    subject="Foldbart navneskilt 86x103mm")
        pageFrame = Frame(0, 0, pageWidth, pageHeight,
                          topPadding=0, bottomPadding=0)
        template = PageTemplate('normal', [pageFrame])
        self.addPageTemplates(template)
