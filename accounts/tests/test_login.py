import pytest

@pytest.mark.django_db
def test_login_success(client, verified_user):

    response = client.post(
        "/api/accounts/login/",
        {
            "email": verified_user.email,
            "password": "123456"
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_unverified_user(client, unverified_user):

    response = client.post(
        "/api/accounts/login/",
        {
            "email": unverified_user.email,
            "password": "123456"
        },
        format="json"
    )
    assert response.status_code == 400
    assert response.data["non_field_errors"][0] == "Verifique seu email antes de fazer login"
    