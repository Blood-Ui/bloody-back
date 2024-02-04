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
    
class DonorUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    blood_group = serializers.CharField(required=False)
    city = serializers.CharField(required=False)

    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone_number', 'date_of_birth', 'blood_group', 'city']

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")

        new_name = validated_data.get("name", instance.name)
        new_email = validated_data.get("email", instance.email)
        new_phone_number = validated_data.get("phone_number", instance.phone_number)
        new_date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        new_blood_group = validated_data.get("blood_group", instance.blood_group_id)
        new_city = validated_data.get("city", instance.city_id)
        if Donor.objects.filter(name=new_name, email=new_email, phone_number=new_phone_number, date_of_birth=new_date_of_birth, blood_group_id=new_blood_group, city_id=new_city).exists():
            raise serializers.ValidationError("Donor already exists")

        instance.name = new_name
        instance.email = new_email
        instance.phone_number = new_phone_number
        instance.date_of_birth = new_date_of_birth
        instance.blood_group_id = new_blood_group
        instance.city_id = new_city
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