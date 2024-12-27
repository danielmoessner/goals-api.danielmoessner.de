from django.core import mail
from django.test import Client
from django.urls import reverse

from apps.users.tests import helpers


def test_password_reset_works(db):
    # setup
    user = helpers.create_user(save=True)
    c = Client()

    # step1: open the password reset page
    response_1 = c.get(reverse("global_form", args=["ResetPassword"]))
    assert 200 == response_1.status_code

    # step2: submit the email on the password reset page and assert email was sent
    response_2 = c.post(
        reverse("global_form", args=["ResetPassword"]), {"email": user.email}
    )
    context = response_2.context
    response_3 = c.get(response_2.url)
    assert response_3.status_code == 200
    assert 1 == len(mail.outbox)

    # step3: click the link within the email and submit new passwords
    token = context[0]["token"]
    uid = context[0]["uid"]
    url = reverse("password_reset_confirm", kwargs={"token": token, "uidb64": uid})
    response_4 = c.get(url, follow=True)
    assert response_4.status_code == 200
    url = reverse(
        "password_reset_confirm", kwargs={"token": "set-password", "uidb64": uid}
    )
    response_5 = c.post(
        url, {"new_password1": "qwe1234!", "new_password2": "qwe1234!"}, follow=True
    )

    # step4: check that the complete page renders
    assert response_5.status_code == 200

    # check user new password works
    user.refresh_from_db()
    assert not user.check_password("pass1234!")
    assert user.check_password("qwe1234!")
