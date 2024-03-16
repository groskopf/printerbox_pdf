
import json
from enum import Enum
from os import access
from typing import List, Optional
from fastapi import HTTPException, Security, status 
from fastapi.security import SecurityScopes
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from pydantic import BaseModel

from printer_code import PrinterCode

API_KEY_NAME = "access_token"


class AccessScope(str, Enum):
    _ADMIN = "admin"
    _PRINTER = "printer"
    _PRINTER_BOOKING = "printer_booking"
    _CONFERENCE = "conference"


class AccessKey(BaseModel):
    key: str
    scopes: List[AccessScope]
    printer_code: Optional[PrinterCode] = None


key_database : List[AccessKey] = []


def load_key_database():
    f = open('keys/keys.json')
    data = json.load(f)
    f.close()
  
    for access_key in data['access_keys']:
        ak = AccessKey(key=access_key['key'], scopes=access_key['scopes'])
        if 'printer_code' in access_key:
            ak.printer_code = access_key['printer_code']
        key_database.append(ak)
        
load_key_database()


api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


def keyHasRequiredRole(current_key : AccessKey, required_scopes : List[AccessScope]):
    #Find key in database
    for access_key in key_database:
        if access_key.key == current_key:
            # Is it an admin key
            if AccessScope._ADMIN in access_key.scopes:
                    return True
            # Do key have required scope
            for scope in required_scopes:
                if scope in access_key.scopes:
                    return True
    return False

def printerKeyHasRequiredRole(current_key : AccessKey, required_scopes : List[AccessScope], printer_code):
    #Find key in database
    for access_key in key_database:
        if access_key.key == current_key:
            # Is it an admin key
            if AccessScope._ADMIN in access_key.scopes:
                    return True
            # Do key have required scope
            for scope in required_scopes:
                if scope in access_key.scopes:
                    if access_key.printer_code and access_key.printer_code == printer_code:
                        return True
    return False


def authenticate_api_key( required_scopes: SecurityScopes = None,
    api_key_query: str = Security(dependency=api_key_query),
    api_key_header: str = Security(dependency=api_key_header),
) -> str:
    if api_key_query and keyHasRequiredRole(api_key_query, required_scopes.scopes):
        return api_key_query
    elif api_key_header and keyHasRequiredRole(api_key_header, required_scopes.scopes):
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not authenticate API key for this endpoint "
        )

def authenticate_printer_api_key( required_scopes: SecurityScopes = None,
    api_key_query: str = Security(dependency=api_key_query),
    api_key_header: str = Security(dependency=api_key_header),
    printer_code : PrinterCode = ""
) -> str:
    if api_key_query and printerKeyHasRequiredRole(api_key_query, required_scopes.scopes, printer_code):
        return api_key_query
    elif api_key_header and printerKeyHasRequiredRole(api_key_header, required_scopes.scopes, printer_code):
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not authenticate API key for this endpoint "
        )