from rest_framework import serializers
from api.models import Patient, Blood_Group, City, Request
from api.utils import RequestStatus


class PatientCreateSerializer(serializers.ModelSerializer):
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

        Request.objects.create(patient_id=patient.id, status=RequestStatus.OPEN.value, created_by_id=user_id, updated_by_id=user_id)
        return patient
    
    def validate_blood_group(self, value):
        if not Blood_Group.objects.filter(id=value).exists():
            raise serializers.ValidationError("Blood Group does not exist")
        return value
    
    def validate_city(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError("City does not exist")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id

        return representation
    
class PatientListSerializer(serializers.ModelSerializer):
    blood_group = serializers.CharField(source='blood_group.name')
    city = serializers.CharField(source='city.name')
    updated_by = serializers.CharField(source='updated_by.get_full_name')
    created_by = serializers.CharField(source='created_by.get_full_name')

    class Meta:
        model = Patient
        fields = '__all__'

class PatientDropDownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['id', 'name']