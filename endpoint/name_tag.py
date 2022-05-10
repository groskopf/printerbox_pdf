'''
Created on 8. maj 2022

@author: paul
'''

from flask_restful import reqparse
from flask.globals import request
from typing import List

from pdf.Layouts import NameData
from pdf.NameTag4786103 import createNameTag4786103

def postNameTag(layout : str, nameData: List[NameData]):
    filename =  'printer_queue/' + '4786103.pdf'
    createNameTag4786103(filename, layout, nameData)
    return { "file_name" : filename}
    