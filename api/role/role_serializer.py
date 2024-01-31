import uuid
from rest_framework import serializers
from api.models import Role

class RoleDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']
