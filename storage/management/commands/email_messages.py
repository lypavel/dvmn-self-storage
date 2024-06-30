from django.urls import reverse

from self_storage.settings import HOST_URL


SUBJECTS = {
    'expiring_rent': 'Ваша аренда скоро закончится',
    'expired_rent': 'Срок вашей аренды истёк',
}

PROFILE_PAGE = reverse('storage:profile')

MESSAGE_ENDING = 'С уважением, компания SelfStorage.'

MONTH_NAMES = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря',
}


def log_success(email):
    return f'Сообщение успешно отправлено: {email}'


def format_date(date):
    month_name = MONTH_NAMES[date.month]
    return f'{date.day} {month_name} {date.year} г.'


def greeting(name=None):
    if not name:
        return 'Здравствуйте.'
    return f'Здравствуйте, {name}.'


def user_profile(profile_url):
    return (
        f'Управление арендой: {HOST_URL}{profile_url}'
    )


def box_info(box_number, storage_address, expiring_date):
    return (
        f'Информация об аренде:\n'
        f'Бокс №{box_number}\n'
        f'Адрес хранилища: {storage_address}\n'
        f'Дата окончания: {format_date(expiring_date)}'
    )


def expiration_message(user_name,
                       box_number,
                       storage_address,
                       expiring_date):
    return (
        f'{greeting(user_name)}\n\n'
        f'Напоминаем, что срок аренды вашего бокса подходит к концу.\n\n'
        f'{box_info(box_number, storage_address, expiring_date)}\n\n'
        f'Если вы не заберёте свои вещи до {format_date(expiring_date)}, '
        'то Вы будете переведены на повышенный тариф, а после '
        'шести месяцев нам придётся их утилизировать.\n\n'
        f'{user_profile(PROFILE_PAGE)}\n\n'
        f'{MESSAGE_ENDING}'
    )


def expired_message(user_name,
                    box_number,
                    storage_address,
                    expiring_date,
                    terminate_date):
    return (
        f'{greeting(user_name)}\n\n'
        f'Напоминаем, что срок аренды вашего бокса подошёл к концу.\n\n'
        f'{box_info(box_number, storage_address, expiring_date)}\n\n'
        'Вы были переведены на повышенный тариф.\n'
        f'Если вы не заберёте свои вещи до {format_date(terminate_date)} '
        'или не продлите аренду, то они будут утилизированы.\n\n'
        f'{user_profile(PROFILE_PAGE)}\n\n'
        f'{MESSAGE_ENDING}'
    )
