import os
from typing import List
import pytest
from datetime import date as date
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from pdf.sheet_type import SheetType
from pdf.name_tag_type import NameTagType

client = TestClient(app)


def test_get_layouts_name_tag():

    # Do name tag type have at least one layout entry?
    for nameTagType in NameTagType:
        response = client.get('layouts/name_tags/' + nameTagType, headers={'access_token': '123admin'})
        assert response.status_code == 200
        
        assert nameTagType == response.json()['name_tag_type']

        nameTagLayouts = response.json()['layouts']
        assert nameTagLayouts
        assert len(nameTagLayouts)



def test_layouts_get_name_tags():
    response = client.get('layouts/name_tags', headers={'access_token': '123admin'})
    assert response.status_code == 200

    nameTagLayoutsList = response.json()

    # Do all name tag types have at least one layout entry?
    for nameTagType in NameTagType:
        nameTagLayouts = next(
            (nameTagLayouts for nameTagLayouts in nameTagLayoutsList
             if nameTagLayouts['name_tag_type'] == nameTagType), None)
        assert nameTagLayouts
        assert len(nameTagLayouts['layouts'])

    # Do any tag types appears more than once?
    for nameTagType in NameTagType:
        assert 1 == len(
            [
                (nameTagLayouts for nameTagLayouts in nameTagLayoutsList
                 if nameTagLayouts['name_tag_type'] == nameTagType)
            ]
        )


def test_get_layouts_sheet():

    # Do name tag type have at least one layout entry?
    for sheetType in SheetType:
        response = client.get('layouts/sheets/' + sheetType, headers={'access_token': '123admin'})
        assert response.status_code == 200
        
        assert sheetType == response.json()['sheet_type']

        sheetLayouts = response.json()['layouts']
        assert sheetLayouts
        assert len(sheetLayouts)


def test_get_layouts_sheets():
    response = client.get('layouts/sheets', headers={'access_token': '123admin'})
    assert response.status_code == 200

    sheetLayoutsList = response.json()

    # Do all name tag types have at least one layout entry?
    for sheetType in SheetType:
        sheetLayouts = next(
            (sheetLayouts for sheetLayouts in sheetLayoutsList
             if sheetLayouts['sheet_type'] == sheetType), None)
        assert sheetLayouts
        assert len(sheetLayouts['layouts'])

    # Do any tag types appears more than once?
    for sheetType in SheetType:
        assert 1 == len(
            [
                (sheetLayouts for sheetLayouts in sheetLayoutsList
                 if sheetLayouts['sheet_type'] == sheetType)
            ]
        )


def test_get_layouts_name_tags():
    response = client.get('layouts/name_tags', headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/name_tags', headers={'access_token': '456printer'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('layouts/name_tags', headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/name_tags', headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_layouts_sheets():
    response = client.get('layouts/sheets', headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/sheets', headers={'access_token': '456printer'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('layouts/sheets', headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/sheets', headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_get_layouts_name_tags():
    response = client.get('layouts/name_tags/' + NameTagType._4786103, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/name_tags/' + NameTagType._4786103, headers={'access_token': '456printer'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('layouts/name_tags/' + NameTagType._4786103, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/name_tags/' + NameTagType._4786103, headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
def test_get_layouts_sheets():
    response = client.get('layouts/sheets/' + SheetType._454880, headers={'access_token': '123admin'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/sheets/' + SheetType._454880, headers={'access_token': '456printer'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.get('layouts/sheets/' + SheetType._454880, headers={'access_token': '789conference'})
    assert response.status_code == status.HTTP_200_OK
    response = client.get('layouts/sheets/' + SheetType._454880, headers={'access_token': 'xyzbooking'})
    assert response.status_code == status.HTTP_403_FORBIDDEN