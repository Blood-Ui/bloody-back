from rest_framework import serializers
from api.models import Patient


class PatientCreateUpdateSerializer(serializers.ModelSerializer):
    blood_group = serializers.CharField(required=True)
    city = serializers.CharField(required=True)

    class Meta:
        model = Patient
        fields = ['name', 'bystander_name', 'bystander_phone_number', 'hospital_name', 'blood_group', 'city']

    def create(self, validated_data):
        user_id = self.context["user_id"]

        validated_data["blood_group_id"] = validated_data.pop("blood_group")
        validated_data["city_id"] = validated_data.pop("city")
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        patient = Patient.objects.create(**validated_data)
        return patient
    
    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")

        instance.name = validated_data.get("name", instance.name)
        instance.bystander_name = validated_data.get("bystander_name", instance.bystander_name)
        instance.bystander_phone_number = validated_data.get("bystander_phone_number", instance.bystander_phone_number)
        instance.hospital_name = validated_data.get("hospital_name", instance.hospital_name)
        instance.blood_group_id = validated_data.get("blood_group", instance.blood_group_id)
        instance.city_id = validated_data.get("city", instance.city_id)
        instance.updated_by_id = user_id
        instance.save()
        return instance

