import sys

from django.core.management.base import BaseCommand

from storage.models import Rent


class Command(BaseCommand):
    help = 'Find all rents with given promo_code and return its count.'

    def add_arguments(self, parser):
        parser.add_argument('promo_code', type=str, help='Promo code')

    def handle(self, *args, **kwargs):

        promo_code = kwargs['promo_code']

        rents_with_promo_code = Rent.objects.filter(promo_code=promo_code)

        print(f'Количество использований промокода {promo_code}: '
              f'{rents_with_promo_code.count()}', file=sys.stdout)
