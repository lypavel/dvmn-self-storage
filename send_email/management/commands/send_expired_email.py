from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.timezone import make_aware

from self_storage import settings
from storage.models import Rent
from send_email.email_messages import SUBJECTS, expired_message, log_success


class Command(BaseCommand):
    help = 'Send email notifications for expired rents'

    def handle(self, *args, **kwargs):
        today = make_aware(datetime.now())
        days_remain = (30, 60, 90, 120, 150, 180)

        sending_dates = [
            make_aware(datetime.now() - timedelta(days=days))
            for days in days_remain
        ]

        query = Q(end_date=today.date() - relativedelta(days=1))
        for sending_date in sending_dates:
            query.add(Q(end_date=sending_date.date()), Q.OR)

        expired_rents = Rent.objects\
            .filter(query)\
            .select_related('box', 'box__storage', 'user')

        expired_rents.update(rent_status='expired')

        for rent in expired_rents:
            self.send_expiration_email(rent)

    def send_expiration_email(self, rent):
        user_email = rent.user.email
        subject = SUBJECTS['expired_rent']
        message = expired_message(
            rent.user.first_name,
            rent.box.number,
            rent.box.storage.address,
            rent.end_date,
            rent.end_date + relativedelta(months=6)
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
