from fastapi import HTTPException, status

class ResourceNotFoundException(HTTPException):
    def __init__(self, type="Resource"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{type} not found")    