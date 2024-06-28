from datetime import date
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django import template

register = template.Library()


@register.filter(name='final_date')
def final_date(end_date):
    return end_date + relativedelta(months=6)


@register.filter(name='days_remain')
def is_expiring(end_date):
    days_remain = end_date - date.today()
    return days_remain.days
