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
        
class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, 
                         detail="You don't have permission to use this function.")
        
class ForbiddenOperationException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, 
                         detail="This operation cannot be executed")

class DuplicatedResourceException(HTTPException):
    def __init__(self, type:str = "Resource"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"{type} already existed")
        
class UnknownException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail="Something went wrong.")
        
def handle_unknown_exception(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except:
            raise UnknownException()
    return decorate