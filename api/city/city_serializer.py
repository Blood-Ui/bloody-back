from rest_framework import serializers
from api.models import City

class CityCreateSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source='district.name')

    class Meta:
        model = City
        fields = ['name', 'district']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["district_id"] = validated_data.pop("district")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        city = City.objects.create(**validated_data)
        return city
    
    def validate(self, data):
        if City.objects.filter(name=data['name'], district=data['district']).exists():
            raise serializers.ValidationError("City already exists")
        return data