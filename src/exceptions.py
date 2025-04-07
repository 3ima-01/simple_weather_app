from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    details = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.details)


class InvalidToken(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    details = "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
