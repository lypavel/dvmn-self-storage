import random
from io import BytesIO

import qrcode
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from self_storage import settings
from storage.coordinates import calculate_delivery_price, fetch_coordinates
from storage.models import Rent

User = get_user_model()

@shared_task
def send_qr_to_email(user_id, rent_id):
    rent = Rent.objects.get(pk=rent_id)
    user = User.objects.get(pk=user_id)

    box = rent.box
    storage = box.storage
    user_coordinates = fetch_coordinates(
        apikey=settings.GEO_API_KEY,
        address=user.address
    )

    if user_coordinates:
        delivery_price = calculate_delivery_price(
            user_coords=user_coordinates,
            storage_coordinates=(storage.latitude, storage.longitude)
        )
        delivery_price = round(delivery_price, 2)
    else:
        delivery_price = None

    password = generate_password()
    box.password = password
    box.save()

    yandex_maps_link = f'https://yandex.ru/maps/?ll={storage.latitude}%2C{storage.longitude}&z=20'

    message_text = f'''
    Адрес: {storage.address}\n
    На карте: {yandex_maps_link}\n
    Пароль: {password}\n
    Доставка до вашего адреса: {f"{delivery_price}р" if delivery_price else 'Невозможно'}
    Доступен до: {rent.end_date}
    '''

    qr_image = qrcode.make(message_text)

    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    subject = "Ваш QR-код для доступа к складу"
    html_message = f"""
        <html>
        <body>
            <p>Уважаемый пользователь,</p>
            <p>Пожалуйста, найдите ваш QR-код для доступа к складу:</p>
            <p>Спасибо, что выбрали наш сервис!</p>
        </body>
        </html>
        """

    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.attach_alternative(html_message, "text/html")

    email.attach('qr_code.png', qr_buffer.read(), 'image/png')

    email.send()


def generate_password(length=6) -> str:
    numbers = [str(i) for i in range(10)]
    return ''.join(random.choices(numbers, k=length))
