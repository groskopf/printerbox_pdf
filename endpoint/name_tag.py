from endpoint.name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_type import NameTagType
from pdf.name_tag_4786103 import createNameTag4786103


def postNameTag(nameTagType: NameTagType, layout: Layout, nameData: NameData):
    filename = 'printer_queue/' + nameTagType.name + \
        '.pdf'  # TODO add random name here

    match nameTagType:
        case NameTagType._4786103:
            createNameTag4786103(filename, layout, nameData)
        case _:
            filename = None

    return {"file_name": filename}
