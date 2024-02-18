from rest_framework.response import Response
from rest_framework import status
from enum import Enum
from rest_framework_simplejwt.authentication import JWTAuthentication
import io
from openpyxl import load_workbook
from django.utils.translation import gettext_lazy as _


class CustomResponse():
    def __init__(self, message=None, data=None):
        self.message = {} if message is None else message
        self.data = {} if data is None else data

    def success_response(self):
        self.error = False
        self.status_code = status.HTTP_200_OK
        return Response({"error": self.error, "message": self.message, "data": self.data, "status_code": self.status_code}, status=self.status_code)
    
    def failure_reponse(self):
        self.error = True
        self.status_code = status.HTTP_400_BAD_REQUEST
        return Response({"error": self.error, "message": self.message, "data": self.data, "status_code": self.status_code}, status=self.status_code)
    
def get_user_id(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        # unpacking
        user , token = response
        user_id = token.payload['user_id']
        return user_id
    return None

def get_user_role(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        # unpacking
        user , token = response
        user_role = token.payload['roles']
        return user_role
    return None

class RequestStatus(Enum):
    OPEN = 'open'
    INPROGRESS = 'in_progress'
    APPROVED = 'approved'
    CANCELLED = 'cancelled'
    CLOSED = 'closed'

    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]
    
class RoleList(Enum):
    ADMIN = 'admin'
    INCHARGE = 'incharge'
    NORMAL_USER = 'normal_user'

    @classmethod
    def get_all_values(cls):
        return [member.value for member in cls]
    
def allowed_roles(allowed_roles):
    def decorator(func):
        def wrapper(obj, request, *args, **kwargs):
            user_roles = get_user_role(request) 
            flag = False
            for user_role in user_roles:
                if user_role in allowed_roles:
                    return func(obj, request, *args, **kwargs)
            if not flag:
                return CustomResponse(message="You don't have permission to perform this action").failure_reponse()
        return wrapper
    return decorator

def get_excel_data(excel_file):
    # Read the file in a memory-efficient way
    file_buffer = io.BytesIO(excel_file.read())
    wb = load_workbook(file_buffer)
    worksheet = wb.active
    excel_data = []
    for row in worksheet.iter_rows(values_only=True):
        # Check for empty rows before processing
        if any(cell for cell in row):  # Use zip_longest to handle potentially different header/data lengths
            row_data = {header.value: cell for header, cell in zip(worksheet[1], row) if cell is not None}
            excel_data.append(row_data)

    return excel_data