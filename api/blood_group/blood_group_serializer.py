import uuid
from rest_framework import serializers
from api.models import Blood_Group
from auth_setup.models import User


class BloodGroupDropDownSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Blood_Group
        fields = ['id', 'name']

class BloodGroupListSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Blood_Group
        fields = '__all__'

class BloodGroupCreateEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blood_Group
        fields = ['name']

    def create(self, validated_data):
        user_id = self.context["user_id"]
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        blood_group = Blood_Group.objects.create(**validated_data)
        return blood_group
