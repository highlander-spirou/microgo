"""
Global error declarations
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Code(str, Enum):
    User_notfound = "User not found"
    JWT_Error = "JWT sign failed"
    File_Unauth = "File Unauthenticated"
    Upload_Error = "Upload Image Error"


@dataclass
class Error:
    """
    Custome error class for a granule control of the code base
    """
    err_code: Code
    message: Optional[str] = None
    

