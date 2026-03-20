from app.responses.base import BaseResponse

class SuccessOK(BaseResponse):
    status_code = 200
    message = "Thành công"

class SuccessCreated(BaseResponse):
    status_code = 201
    message = "Gọi món thành công"