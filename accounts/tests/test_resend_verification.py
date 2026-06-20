import pytest
from django.utils import timezone
from unittest.mock import patch

@pytest.mark.django_db
def test_resend_verification_email_success(client, unverified_user):

    response = client.post(
        "/api/accounts/resend-verification/",
        {
            "email": unverified_user.email
        },
        format="json"
    )

    unverified_user.refresh_from_db()

    assert response.status_code == 200
    assert response.data["message"] == "Email de verificação reenviado"
    assert unverified_user.last_verification_email is not None

@pytest.mark.django_db
@patch("accounts.views.send_mail")
def test_password_reset_rate_limit(mock_send_mail, user, client):
    user.last_password_reset_request = timezone.now()
    user.save()

    response = client.post(
        "/api/accounts/password-reset/",
        {
            "email": user.email
        },
        format="json"
    )

    assert response.status_code == 429
    assert "aguarde" in response.data["error"].lower()

    mock_send_mail.assert_not_called()