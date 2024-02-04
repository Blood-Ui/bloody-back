from rest_framework import serializers
from api.models import Donor, Blood_Group, City

class DonorCreateSerializer(serializers.ModelSerializer):
    blood_group = serializers.CharField(required=True)
    city = serializers.CharField(required=True)

    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone_number', 'date_of_birth', 'blood_group', 'city']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["blood_group_id"] = validated_data.pop("blood_group")
        validated_data["city_id"] = validated_data.pop("city")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        donor = Donor.objects.create(**validated_data)
        return donor
    
    def validate_blood_group(self, value):
        if not Blood_Group.objects.filter(id=value).exists():
            raise serializers.ValidationError("Blood Group does not exist")
        return value
    
    def validate_city(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError("City does not exist")
        return value
    
class DonorListSerializer(serializers.ModelSerializer):
    blood_group = serializers.CharField(source='blood_group.name')
    city = serializers.CharField(source='city.name')
    district = serializers.CharField(source='city.district.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Donor
        fields = ['id', 'name', 'phone_number', 'email', 'date_of_birth', 'blood_group', 'city', 'district', 'updated_by', 'created_by', 'updated_at', 'created_at']

class DonorDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['id', 'name']