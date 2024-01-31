import uuid
from rest_framework import serializers
from api.models import Blood_Group
from auth_setup.models import User


class BloodGroupDropDownSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Blood_Group
        fields = ['id', 'name']
