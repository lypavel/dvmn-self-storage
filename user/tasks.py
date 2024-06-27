from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from self_storage import settings


@shared_task
def send_message_to_email(user_email: str, token, uid):
    data = {
        'token': token,
        'uid': uid
    }
    subject = 'Подтверждение почты'
    html_message = render_to_string(
        'user/email.html',
        {
            'data': data,
            'host': settings.HOST_URL
        }
    )
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )

    email.attach_alternative(html_message, "text/html")
    email.send()
