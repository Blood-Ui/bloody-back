from rest_framework.response import Response
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