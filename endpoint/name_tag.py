'''
Created on 8. maj 2022

@author: paul
'''

from endpoint.name_data import NameData
from pdf.layouts import Layout
from pdf.name_tag_4786103 import createNameTag4786103

def postNameTag(layout : Layout, nameData: NameData):
    filename =  'printer_queue/' + '4786103.pdf'
    createNameTag4786103(filename, layout, nameData)
    return { "file_name" : filename}
    