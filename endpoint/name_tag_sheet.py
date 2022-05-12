'''
Created on 8. maj 2022

@author: paul
'''
from typing import List

from endpoint.name_data import NameData
from pdf.name_tag_sheet_456090 import createNameTagSheet456090

def postNameTagSheet(layout : str, nameDataList: List[NameData]):
    filename =  'printer_queue/' + '456090.pdf'
    createNameTagSheet456090(filename, layout, nameDataList);
    return { "file_name" : filename}