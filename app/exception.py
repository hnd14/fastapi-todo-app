from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, type="Resource"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{type} not found")    
        
class InvalidActionException(HTTPException):
    def __init__(self, msg:str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
        
class JWTTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT Token")
        
class AuthenticationFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, 
                         detail="Authentication failed. Please double check your username and password.")