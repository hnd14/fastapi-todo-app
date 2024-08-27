from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, type="Resource"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{type} not found")    
        
class InvalidActionException(HTTPException):
    def __init__(self, msg:str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)