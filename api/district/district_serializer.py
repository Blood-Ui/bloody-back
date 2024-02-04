from rest_framework import serializers
from api.models import District


class DistrictCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['name']

    def create(self, validated_data):
        user_id = self.context["user_id"]
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        district = District.objects.create(**validated_data)
        return district
    
    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")
        instance.name = validated_data.get("name", instance.name)
        instance.updated_by_id = user_id
        instance.save()
        return instance

    def validate(self, data):
        if District.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError("District already exists")
        return data

class DistrictListSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = District
        fields = '__all__'

class DistrictDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']