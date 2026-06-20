import pytest
from unittest.mock import patch
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@pytest.mark.django_db
@patch("accounts.views.send_mail")
def test_password_reset_request_success(mock_send_mail, client, user):

    response = client.post(
        "/api/accounts/password-reset/",
        {
            "email": user.email
        },
        format="json"
    )

    assert response.status_code == 200
    assert "redefinir sua senha" in response.data["message"]

    mock_send_mail.assert_called_once()


@pytest.mark.django_db
def test_password_reset_request_email_not_found(client):

    response = client.post(
        "/api/accounts/password-reset/",
        {
            "email": "naoexiste@gmail.com"
        },
        format="json"
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_password_reset_confirm_success(user, client):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.post(
        f"/api/accounts/password-reset-confirm/{uid}/{token}/",
        {
            "password": "nova123",
            "password2": "nova123"
        },
        format="json"
    )

    user.refresh_from_db()

    assert response.status_code == 200
    assert response.data["message"] == "Senha redefinida com sucesso"

    assert user.check_password("nova123")

@pytest.mark.django_db
def test_password_reset_confirm_password_mismatch(client, user):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    response = client.post(
        f"/api/accounts/password-reset-confirm/{uid}/{token}/",
        {
            "password": "nova123",
            "password2": "outrasenha"
        },
        format="json"
    )

    assert response.status_code == 400
    assert response.data["error"] == "As senhas não coincidem"

