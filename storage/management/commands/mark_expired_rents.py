from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from storage.models import Rent

from django.db import transaction


class Command(BaseCommand):
    help = 'Find all expired rents and change its status.'

    @transaction.atomic()
    def handle(self, *args, **kwargs):
        today = make_aware(datetime.now())
        Rent.objects\
            .exclude(rent_status__in=('expired', 'inactive'))\
            .filter(end_date__lt=today)\
            .update(rent_status='expired')
