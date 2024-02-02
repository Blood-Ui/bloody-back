from rest_framework import serializers
from api.models import Donor, Blood_Group, City

class DonorCreateSerializer(serializers.ModelSerializer):
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
    
    def validate_blood_group(self, value):
        if not Blood_Group.objects.filter(id=value).exists():
            raise serializers.ValidationError("Blood Group does not exist")
        return value
    
    def validate_city(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError("City does not exist")
        return value