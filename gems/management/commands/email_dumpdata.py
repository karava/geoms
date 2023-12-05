from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from io import StringIO

class Command(BaseCommand):
    help = 'Emails the output of dumpdata for a specified app or all apps'

    def add_arguments(self, parser):
        parser.add_argument('app', nargs='?', type=str, help='App label')

    def handle(self, *args, **options):
        app_label = options['app']
        data = StringIO()

        if app_label:
            call_command('dumpdata', app_label, stdout=data)
        else:
            call_command('dumpdata', stdout=data)

        data.seek(0)

        email_subject = f'Data Dump of {"All Apps" if not app_label else app_label}'
        email = EmailMessage(
            subject=email_subject,
            body=f'Attached is the data dump of {"all apps" if not app_label else app_label}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['kish@geosynthetics.net.au']  # Replace with the recipient's email
        )
        email.attach(f'{"all_apps" if not app_label else app_label}_dump.json', data.getvalue(), 'application/json')
        email.send()

        self.stdout.write(self.style.SUCCESS(f'Successfully sent the data email for {"all apps" if not app_label else app_label}'))