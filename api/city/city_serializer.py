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
    
    def validate_district(self, value):
        if not City.objects.filter(district=value).exists():
            raise serializers.ValidationError("District does not exist")
        return value
    
class CityListSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source='district.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = City
        fields = '__all__'

class CityUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name')

    class Meta:
        model = City
        fields = ['name']

        def update(self, instance, validated_data):
            user_id = self.context.get("user_id")
            new_name = validated_data.get("name")
            if City.objects.filter(name=new_name).exists():
                raise serializers.ValidationError("City already exists")
            instance.name = new_name
            instance.updated_by_id = user_id
            instance.save()
            return instance