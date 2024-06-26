from django.urls import path

from storage.views import index, faq

app_name = 'storage'

urlpatterns = [
    path('', index, name='index'),
    path('faq', faq, name='faq'),
]
