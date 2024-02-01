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
