import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import make_aware

from self_storage import settings
from storage.models import Rent


class Command(BaseCommand):
    help = 'Send email notifications for expired rents'

    def handle(self, *args, **kwargs):
        tomorrow = make_aware(datetime.datetime.now() + datetime.timedelta(days=1))

        expiring_rents = Rent.objects.filter(
            end_date=tomorrow.date()
        ).select_related('box')

        for rent in expiring_rents:
            self.send_expiration_email(rent)

    def send_expiration_email(self, rent):
        subject = 'Срок окончания аренды'
        message = f'Срок аренды вашей ячейки {rent.box.number} истек'
        recipient_list = [rent.user.email]
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list
        )
        self.stdout.write(self.style.SUCCESS(f'Сообщение отправление успешно пользователю {rent.user.email}'))
