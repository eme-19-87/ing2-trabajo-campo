"""Type definitions for data structures used in the application."""

from datetime import date
from typing import TypedDict
from numpy import double


class UserData(TypedDict):
    """Type definition for customer dimension"""
    fname:str
    lname: str
    email:str
    dni: str
    password:str
    id_rol:int
    active: bool
