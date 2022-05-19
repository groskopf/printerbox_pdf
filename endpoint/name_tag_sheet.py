import uuid
from typing import List

from endpoint.name_data import NameData
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf.name_tag_sheet_456090 import createNameTagSheet456090

def postNameTagSheet(nameTagSheetType : NameTagSheetType, layout : str, nameDataList: List[NameData]):
    filename =  'printer_queue/' + nameTagSheetType + '_' + uuid.uuid4().hex + '.pdf'  # TODO add random name here

    match nameTagSheetType:
        case NameTagSheetType._456090:
            createNameTagSheet456090(filename, layout, nameDataList);
        case _:
            filename = None

    return { "file_name" : filename}