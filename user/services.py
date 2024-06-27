from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode


def generate_uid_with_token(user):
    token = default_token_generator.make_token(user)
    uid = force_str(urlsafe_base64_encode(force_bytes(user.id)))
    return token, uid
