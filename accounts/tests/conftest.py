import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def user():
    
    return User.objects.create_user(
        email="lucas@gmail.com",
        password="123456"
    )

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def verified_user():
    return User.objects.create_user(
        email="lucas@gmail.com",
        password="123456",
        is_verified=True
    )

@pytest.fixture
def unverified_user():
    return User.objects.create_user(
        email="lucas@gmail.com",
        password="123456",
        is_verified=False
    )

@pytest.fixture
def register_payload():
    return {
        "full_name": "Lucas Medeiros",
        "cpf": "12345678900",
        "email": "lucas@gmail.com",
        "password": "123456",
        "password2": "123456"
    }