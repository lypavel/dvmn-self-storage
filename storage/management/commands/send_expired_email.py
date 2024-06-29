from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.timezone import make_aware

from self_storage import settings
from storage.models import Rent


class Command(BaseCommand):
    help = 'Send email notifications for expired rents'

    def handle(self, *args, **kwargs):
        today = make_aware(datetime.now())
        days_remain = (30, 60, 90, 120, 150, 180)

        sending_dates = [
            make_aware(datetime.now() - timedelta(days=days))
            for days in days_remain
        ]

        query = Q(end_date=today.date())
        for sending_date in sending_dates:
            query.add(Q(end_date=sending_date.date()), Q.OR)

        expiring_rents = Rent.objects\
            .filter(query)\
            .select_related('box')\

        expiring_rents.update(rent_status='expired')

        for rent in expiring_rents:
            self.send_expiration_email(rent)

    def send_expiration_email(self, rent):
        subject = 'Срок окончания аренды'
        message = f'Срок аренды вашей ячейки {rent.box.number} истек. Вы были переведены на повышенный тариф. Заберите свои вещи до {rent.end_date + relativedelta(months=6)} или продлите аренду, в противном случае ваши вещи будут утилизированы.'
        recipient_list = [rent.user.email]
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list
        )
        self.stdout.write(self.style.SUCCESS(f'Сообщение отправление успешно пользователю {rent.user.email}'))
