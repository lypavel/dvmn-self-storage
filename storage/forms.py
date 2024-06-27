from django import forms

from .models import Consultation


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
