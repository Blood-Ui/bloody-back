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
    

class CustomResponse(Response):
    def __init__(self, error=None, message=None, data=None, status_code=None, *args, **kwargs):
        self.error = '' if error is None else error
        self.message = {} if message is None else message
        self.data = {} if data is None else data
        self.status_code = status.HTTP_200_OK if status_code is 1 else status.HTTP_400_BAD_REQUEST

        return super().__init__(data = {'error': self.error, 'message': self.message, 'data': self.data, 'status_code': self.status_code}, status=self.status_code, *args, **kwargs)