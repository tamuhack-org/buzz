from fastapi import HTTPException


class CustomError(HTTPException):
    def __init__(
        self,
        message: str,
        status_code: int,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message, headers=headers)


class BadRequest(CustomError):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(message=message, status_code=400)


class Unauthorized(CustomError):
    def __init__(self, message: str = "Unauthorized", realm: str | None = None) -> None:
        headers = {"WWW-Authenticate": f'Bearer realm="{realm or "api"}"'}
        super().__init__(message=message, status_code=401, headers=headers)


class Forbidden(CustomError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message=message, status_code=403)


class NotFound(CustomError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(message=message, status_code=404)


class Conflict(CustomError):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message=message, status_code=409)


class InternalServerError(CustomError):
    def __init__(self, message: str = "Internal Server Error") -> None:
        super().__init__(message=message, status_code=500)


class ChannelNotFound(NotFound):
    def __init__(self, channel_id: str = "id") -> None:
        super().__init__(message=f"Requested channel ID ({channel_id}) not found.")

class InvalidChannelType(BadRequest):
    def __init__(self, correct_channel_type: str, channel_id: str = "id") -> None:
        super().__init__(message=f"Provided channel ID ({channel_id}) is not of type {correct_channel_type}.")

class MessageNotFound(NotFound):
    def __init__(self, message_id: str = "id", channel_id: str = "id") -> None:
        super().__init__(message=f"Requested message ID ({message_id}) not found in channel: {channel_id}.")
