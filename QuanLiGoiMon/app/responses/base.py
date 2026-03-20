from flask import jsonify

class BaseResponse:
    status_code = 200
    message = ""

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def to_response(self):
        return jsonify({"message": self.message}), self.status_code