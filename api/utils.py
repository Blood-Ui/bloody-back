from rest_framework.response import Response
from rest_framework import status
from enum import Enum

def allowed_roles(allowed_roles):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                return Response({"error": "You don't have permission to perform this action."}, status=403)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

class RequestStatus(Enum):
    OPEN = 'open'
    INPROGRESS = 'in_progress'
    APPROVED = 'approved'
    CANCELLED = 'cancelled'
    CLOSED = 'closed'

    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]

class CustomResponse():
    def __init__(self, message, data):
        self.message = {} if message is None else message
        self.data = {} if data is None else data

    def success_response(self):
        self.error = False
        self.status_code = status.HTTP_200_OK
        return Response({"error": self.error, "message": self.message, "data": self.data, "status_code": self.status_code}, status=self.status_code)