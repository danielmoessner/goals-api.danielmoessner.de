from django.core import mail
from django.test import Client
from django.urls import reverse

from apps.users.tests import helpers


def test_register_works_with_mail(db):
    data = {"new_email": "dummy_new@abc.de"}

    # setup
    user = helpers.create_user(save=True)
    c = Client()
    c.login(email=user.email, password="pass1234!")

    # step1: open the change email page
    response_1 = c.get(reverse("change_email"))
    assert 200 == response_1.status_code

    # step2: submit and check that the new email is saved
    response_2 = c.post(reverse("change_email"), data)
    user.refresh_from_db()
    assert user.new_email == data["new_email"]

    # step3: check that email was send
    assert 1 == len(mail.outbox)

    # # step4: click the link within the email and confirm email
    context = response_2.context
    assert context["link"]
    c.get(context["link"], follow=True)
    user.refresh_from_db()
    assert user.email == data["new_email"]
    assert user.new_email is None
