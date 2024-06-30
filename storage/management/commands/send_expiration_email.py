from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.timezone import make_aware

from self_storage import settings
from storage.models import Rent
from .email_messages import SUBJECTS, expiration_message, log_success


class Command(BaseCommand):
    help = 'Send email notifications for rents expiring in three, seven, '
    'fourteen and thirty days'

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
            .select_related('box', 'box__storage', 'user')

        for rent in expiring_rents:
            self.send_expiration_email(rent)

    def send_expiration_email(self, rent):
        user_email = rent.user.email
        subject = SUBJECTS['expiring_rent']
        message = expiration_message(
            rent.user.username,
            rent.box.number,
            rent.box.storage.address,
            rent.end_date
        )

        recipient_list = [user_email]
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list
        )

        success = log_success(user_email)
        self.stdout.write(self.style.SUCCESS(success))
