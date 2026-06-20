import pytest 
from django.contrib.auth.tokens import default_token_generator

@pytest.mark.django_db
def test_verify_email_success(client,unverified_user):

    token = default_token_generator.make_token(unverified_user)

    response = client.get(
        f"/api/accounts/verify/{unverified_user.id}/{token}/"
    )

    unverified_user.refresh_from_db()

    assert response.status_code == 200
    assert unverified_user.is_verified is True
    assert response.data["message"] == "Email verificado com sucesso!"


@pytest.mark.django_db
def test_verify_email_invalid_token(client, unverified_user):

    response = client.get(
        f"/api/accounts/verify/{unverified_user.id}/token-invalido/"
    )

    unverified_user.refresh_from_db()

    assert response.status_code == 400
    assert unverified_user.is_verified is False
    assert response.data["error"] == "Token inválido"

@pytest.mark.django_db
def test_verify_email_already_verified(client, verified_user):

    token = default_token_generator.make_token(verified_user)

    response = client.get(
        f"/api/accounts/verify/{verified_user.id}/{token}/"
    )

    assert response.status_code == 200
    assert response.data["message"] == "Email já verificado"
