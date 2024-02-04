from rest_framework import serializers
from api.models import City, District

class CityCreateSerializer(serializers.ModelSerializer):
    district = serializers.CharField(required=True)

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
        if not District.objects.filter(id=value).exists():
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
    district = serializers.CharField(required=False)

    class Meta:
        model = City
        fields = ['name', 'district']

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        new_name = validated_data.get("name", instance.name)
        new_district = validated_data.get("district", instance.district_id)
        if City.objects.filter(name=new_name, district=new_district).exists():
            raise serializers.ValidationError("City already exists")
        instance.name = new_name
        instance.district_id = new_district
        instance.updated_by_id = user_id
        instance.save()
        return instance
    
    def validate_district(self, value):
        if not District.objects.filter(id=value).exists():
            raise serializers.ValidationError("District does not exist")
        return value
        
class CityDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']