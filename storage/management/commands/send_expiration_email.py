from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.timezone import make_aware

from self_storage import settings
from storage.models import Rent


class Command(BaseCommand):
    help = 'Send email notifications for rents expiring in one day'

    def handle(self, *args, **kwargs):
        days_left = (3, 7, 14, 30)
        sending_dates = [
            make_aware(datetime.now() + timedelta(days=day))
            for day in days_left
        ]

        query = Q(end_date=sending_dates[0].date())
        for sending_date in sending_dates:
            query.add(Q(end_date=sending_date.date()), Q.OR)

        expiring_rents = Rent.objects\
            .filter(query)\
            .select_related('box')

        for rent in expiring_rents:
            self.send_expiration_email(rent)

    def send_expiration_email(self, rent):
        subject = 'Срок окончания аренды'
        message = f'Срок аренды вашей ячейки {rent.box.number} истекает {rent.end_date}.'
        recipient_list = [rent.user.email]
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list
        )
        self.stdout.write(self.style.SUCCESS(f'Сообщение отправление успешно пользователю {rent.user.email}'))