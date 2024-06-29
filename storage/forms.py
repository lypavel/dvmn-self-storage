from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget

from .models import Consultation, Rent


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': (
                        'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 '
                        'SelfStorage__bg_lightgrey'
                    ),
                    'placeholder': 'Укажите ваш e-mail'
                }
            )
        }


class OrderForm(forms.ModelForm):

    start_date = forms.DateField(
        label='Дата начала*',
        widget=forms.widgets.SelectDateWidget(),
        initial=date.today
    )
    period = forms.IntegerField(
        label='Срок аренды, мес*'
    )
    phone_number = PhoneNumberField(
        label='Номер телефона*',
        region='RU',
        widget=RegionalPhoneNumberWidget(region='RU')
    )
    address = forms.CharField(
        label='Адрес',
        max_length=255,
        required=False
    )
    promo_code = forms.CharField(
        label='Промокод',
        max_length=50,
        required=False
    )

    field_order = ('start_date', 'period', 'phone_number', 'address', 'promo_code')

    class Meta:
        model = Rent
        fields = ('id', 'phone_number', 'address', 'promo_code')
