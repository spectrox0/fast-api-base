from fastapi import HTTPException, status


class AuthorizationException(HTTPException):
    """
    Exception raised for unauthorized access.

    Inherits from `HTTPException` and sets the status code to 401 (Unauthorized)
    with a default detail message of "Unauthorized access".
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access",
        )


class UserLoginException(HTTPException):
    """
    Exception raised when a user fails to login due to an invalid username or password.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


class NotFoundException(HTTPException):
    """
    Exception raised when a resource is not found.

    Args:
        detail (str, optional): Additional detail about the exception.
        Defaults to "Resource not found".
    """

    def __init__(
        self,
        detail: str = "Resource not found",
        resource: str = None,
    ):
        super().__init__(detail)
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource not found: {resource}" if resource else detail,
        )


class BadRequestException(HTTPException):
    """
    Exception raised for a bad request.

    Args:
        detail (str, optional): Additional detail about the exception. Defaults to "Bad request".
    """

    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ForbiddenException(HTTPException):
    """
    Exception raised when a user is forbidden from accessing a resource.

    Args:
        detail (str, optional): Additional detail about the exception. Defaults to "Forbidden".
    """

    def __init__(self, detail: str = "Forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class ConflictException(HTTPException):
    """
    Exception raised for conflicts in the application.

    Attributes:
        detail (str): Additional details about the conflict.
    """

    def __init__(self, detail: str = "Conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class UnprocessableEntityException(HTTPException):
    """
    Exception raised for HTTP 422 Unprocessable Entity errors.

    Args:
        detail (str): Additional detail about the exception. Defaults to "Unprocessable entity".
    """

    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class EmailAlreadyUsedException(HTTPException):
    """
    Exception raised when the provided email is already in use.

    Args:
        detail (str, optional): Additional detail about the exception.
        Defaults to "Email is already in use".
    """

    def __init__(self, detail: str = "Email is already in use"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class ServerErrorException(HTTPException):
    """
    Exception raised when an unexpected server error occurs.

    Args:
        detail (str, optional): Additional detail about the exception.
        Defaults to "Internal server error".
    """

    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
