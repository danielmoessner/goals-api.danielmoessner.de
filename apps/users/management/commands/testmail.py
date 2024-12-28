from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        subject = "Testmail"
        body = "Hallo, das ist eine Testmail."
        email_message = EmailMultiAlternatives(
            subject, body, settings.DEFAULT_FROM_EMAIL, [settings.SERVER_EMAIL]
        )
        email_message.send()
