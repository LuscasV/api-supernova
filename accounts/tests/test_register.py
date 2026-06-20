import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

@pytest.mark.django_db
def test_register_user_success(client, register_payload):

    response = client.post(
        "/api/accounts/register/",
        register_payload,
        format="json"
    )

    assert response.status_code == 201

    user = User.objects.get(email="lucas@gmail.com")

    assert user.email == "lucas@gmail.com"
    assert user.is_verified is False

    profile = Profile.objects.get(user=user)

    assert profile.full_name == "Lucas Medeiros"
    assert profile.cpf == "12345678900"

@pytest.mark.django_db
def test_register_duplicate_cpf(client, register_payload):

    #primeiro cadastro
    client.post(
        "/api/accounts/register/",
        register_payload,
        format="json"
    )

    #segundo cadastro mesmo cpf
    response = client.post(
        "/api/accounts/register/",
        {
            "full_name": "Maria",
            "cpf": "12345678900",
            "email": "maria@gmail.com",
            "password": "123456",
            "password2": "123456"
        },
        format="json"
    )

    assert response.status_code == 400
    assert "cpf" in str(response.data).lower() 

@pytest.mark.django_db
def test_register_password_mismatch(client):

    payload = {
        "full_name": "Lucas",
        "cpf": "12345678900",
        "email": "lucas@email.com",
        "password": "123456",
        "password2": "654321"
    }

    response = client.post(
        "/api/accounts/register/",
        payload,
        format="json"
    )

    assert response.status_code == 400