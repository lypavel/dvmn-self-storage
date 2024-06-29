from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password')


class UserContactsUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number')


class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserInfoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
