from rest_framework import serializers
from api.models import Donor, Blood_Group, City

class DonorCreateUpdateSerializer(serializers.ModelSerializer):
    blood_group = serializers.CharField(required=True)
    city = serializers.CharField(required=True)

    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone', 'date_of_birth', 'blood_group', 'city']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["blood_group_id"] = validated_data.pop("blood_group")
        validated_data["city_id"] = validated_data.pop("city")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        donor = Donor.objects.create(**validated_data)
        return donor
    
    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.blood_group_id = validated_data.get("blood_group", instance.blood_group_id)
        instance.city_id = validated_data.get("city", instance.city_id)
        instance.updated_by_id = user_id
        instance.save()
        return instance
    
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
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Donor
        fields = '__all__'

class DonorDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['id', 'name']