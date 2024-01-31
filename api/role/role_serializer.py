import uuid
from rest_framework import serializers
from api.models import Role, UserRoleLink
from auth_setup.models import User

class RoleDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class RoleListSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Role
        fields = '__all__'

class RoleCreateEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['name']

    def create(self, validated_data):
        user_id = self.context["user_id"]
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        role = Role.objects.create(**validated_data)
        return role
    
    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        instance.name = validated_data.get("name", instance.name)
        instance.updated_by_id = user_id
        instance.save()
        return instance

class UserRoleListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name')
    role = serializers.CharField(source='role.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = UserRoleLink
        fields = '__all__'


class UserRoleCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = UserRoleLink
        fields = ['user', 'role']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["user_id"] = validated_data.pop("user")
        validated_data["role_id"] = validated_data.pop("role")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        user_role = UserRoleLink.objects.create(**validated_data)
        return user_role
    
    def validate(self, data):
        if UserRoleLink.objects.filter(user=data['user'], role=data['role']).exists():
            raise serializers.ValidationError("User Role already exists")
        return data
    
    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Enter a valid user")
        return value
    
    def validate_role(self, value):
        if not Role.objects.filter(id=value).exists():
            raise serializers.ValidationError("Enter a valid role")
        return value