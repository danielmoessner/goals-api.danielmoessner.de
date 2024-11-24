from django.core import mail
from django.test import Client
from django.urls import reverse

from apps.users.tests import helpers


def test_register_works_with_mail(db):
    data = {
        "old_password": "pass1234!!",
        "new_password1": "test1234!!",
        "new_password2": "test1234!!",
    }

    # setup
    user = helpers.create_user(save=True, password=data["old_password"])
    c = Client()
    c.login(email=user.email, password=data["old_password"])

    # step1: open the change email page
    response_1 = c.get(reverse("change_password"))
    assert 200 == response_1.status_code

    # step2: submit and check that the new password is saved and confirmation email sent
    response_2 = c.post(reverse("change_password"), data)
    assert 302 == response_2.status_code
    user.refresh_from_db()
    assert not user.check_password("pass1234!")
    assert user.check_password(data["new_password1"])
    assert 1 == len(mail.outbox)
