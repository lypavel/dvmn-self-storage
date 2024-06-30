from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from user.forms import UserRegisterForm, UserContactsUpdateForm, \
    UserInfoUpdateForm
from user.services import generate_uid_with_token
from user.tasks import send_message_to_email

User = get_user_model()


@transaction.atomic()
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            password = user_data.pop('password')
            email = user_data.pop('email')
            phone_number = user_data.pop('phone_number')
            user = User.objects.create_user(
                password=password,
                email=email,
                phone_number=phone_number,
            )
            token, uid = generate_uid_with_token(user)
            send_message_to_email.delay(
                user_email=email,
                token=token,
                uid=uid
            )
            return redirect(
                reverse('storage:index_after_registration',
                        kwargs={'after_registration': True})
            )

    return render(request, 'registration/registration.html')


def verify_email(request):
    token = request.GET.get('token')
    uid = request.GET.get('uid')
    if not token or not uid:
        return redirect(
            reverse('storage:index_user_verified',
                    kwargs={'user_verified': False})
        )

    pk = force_str(urlsafe_base64_decode(uid))
    user = User.objects.get(pk=pk)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
    return redirect(
        reverse(
            'storage:index_user_verified',
            kwargs={'user_verified': True}
        )
    )


@login_required
def update_profile_info(request):
    if request.method == 'POST':
        form = UserInfoUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
    return redirect(reverse('storage:profile'))


@login_required
def update_profile_contacts(request):
    if request.method == 'POST':
        form = UserContactsUpdateForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            form.save()
    return redirect(reverse('storage:profile'))
