from .models import Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Address

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    cpf = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "cpf",
            "email",
            "password",
            "password2",
        ]

    def validate(self, data):
        if data["password"] !=data["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem"})
        return data
    
    def validate_cpf(self, value):
        if Profile.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF já cadastrado.")
        return value
        
    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        cpf = validated_data.pop("cpf")
        validated_data.pop("password2")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        Profile.objects.create(
            user=user,
            full_name=full_name,
            cpf=cpf
        )

        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "number",
            "neighborhood",
            "city",
            "state",
            "zip_code",
            "is_default",
        ]
    def create(self, validated_data):
        user = validated_data["user"]

        if validated_data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = instance.user

        if validated_data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).exclude(id=instance.id).update(is_default=False)

        return super().update(instance, validated_data)