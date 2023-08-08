from typing import Dict
from fastapi import HTTPException, status

class PostNotFoundException(HTTPException):
    def __init__(
            self,
            status_code: int = status.HTTP_404_NOT_FOUND,
            detail: str = "Post not found",
            headers: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)