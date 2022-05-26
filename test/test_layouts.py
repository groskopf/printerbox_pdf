import os
from typing import List
import pytest
from datetime import date as date
from fastapi.testclient import TestClient

from main import app
from pdf.name_tag_sheet_type import NameTagSheetType
from pdf.name_tag_type import NameTagType

client = TestClient(app)


def test_get_layouts_name_tag():

    # Do name tag type have at least one layout entry?
    for nameTagType in NameTagType:
        response = client.get('layouts/name_tags/' + nameTagType)
        assert response.status_code == 200
        
        assert nameTagType == response.json()['name_tag_type']

        nameTagLayouts = response.json()['layouts']
        assert nameTagLayouts
        assert len(nameTagLayouts)



def test_layouts_get_name_tags():
    response = client.get('layouts/name_tags')
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


def test_get_layouts_name_tag_sheet():

    # Do name tag type have at least one layout entry?
    for nameTagSheetType in NameTagSheetType:
        response = client.get('layouts/name_tag_sheets/' + nameTagSheetType)
        assert response.status_code == 200
        
        assert nameTagSheetType == response.json()['name_tag_sheet_type']

        nameTagSheetLayouts = response.json()['layouts']
        assert nameTagSheetLayouts
        assert len(nameTagSheetLayouts)


def test_get_layouts_name_tag_sheets():
    response = client.get('layouts/name_tags_sheets')
    assert response.status_code == 200

    nameTagSheetLayoutsList = response.json()

    # Do all name tag types have at least one layout entry?
    for nameTagSheetType in NameTagSheetType:
        nameTagSheetLayouts = next(
            (nameTagSheetLayouts for nameTagSheetLayouts in nameTagSheetLayoutsList
             if nameTagSheetLayouts['name_tag_sheet_type'] == nameTagSheetType), None)
        assert nameTagSheetLayouts
        assert len(nameTagSheetLayouts['layouts'])

    # Do any tag types appears more than once?
    for nameTagSheetType in NameTagSheetType:
        assert 1 == len(
            [
                (nameTagSheetLayouts for nameTagSheetLayouts in nameTagSheetLayoutsList
                 if nameTagSheetLayouts['name_tag_sheet_type'] == nameTagSheetType)
            ]
        )
