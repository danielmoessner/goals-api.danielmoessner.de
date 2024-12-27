import pytest
from django.core import mail
from django.test import Client, override_settings
from django.urls import reverse

from apps.users.models import CustomUser


@pytest.fixture
def data():
    yield {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@abc.de",
        "password1": "pass1234!!",
        "password2": "pass1234!!",
    }


def test_register_works(db, data):
    c = Client()
    with override_settings(CUSTOM_ALLOW_REGISTRATION=True):
        response = c.post(reverse("global_form", args=["Register"]), data=data)
    assert response.status_code == 302
    assert CustomUser.objects.filter(email=data["email"]).exists()


def test_register_works_with_mail(db, data):
    # setup
    c = Client()

    # step1: open the register page
    response_1 = c.get(reverse("global_form", args=["Register"]))
    assert 200 == response_1.status_code

    # step2: submit and check that user exists
    with override_settings(CUSTOM_ALLOW_REGISTRATION=True):
        response_2 = c.post(reverse("global_form", args=["Register"]), data)
    response_3 = c.get(response_2.url)
    assert response_3.status_code == 200
    assert CustomUser.objects.filter(email=data["email"]).exists()
    assert not CustomUser.objects.get(email=data["email"]).email_confirmed

    # step3: check that email was send
    assert 1 == len(mail.outbox)

    # step4: click the link within the email and confirm email
    context = response_2.context
    assert context["link"]
    response_4 = c.get(context["link"], follow=True)
    assert response_4.status_code == 200
    assert CustomUser.objects.get(email=data["email"]).email_confirmed
