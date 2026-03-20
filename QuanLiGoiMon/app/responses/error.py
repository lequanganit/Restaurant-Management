from app.responses.base import BaseResponse

class ErrorResponse(BaseResponse, Exception):
    status_code = 500
    message = "Lỗi hệ thống"

class NotAuthenticatedError(ErrorResponse):
    status_code = 401
    message = "Chưa đăng nhập"

class TableNotFoundError(ErrorResponse):
    status_code = 404
    message = "Bàn không tồn tại"

class EmptyCartError(ErrorResponse):
    status_code = 400
    message = "Giỏ hàng trống"