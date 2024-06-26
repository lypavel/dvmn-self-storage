from django.urls import path

from storage.views import boxes, index, faq, profile

app_name = 'storage'

urlpatterns = [
    path('', index, name='index'),
    path('faq', faq, name='faq'),
    path('boxes', boxes, name='boxes'),
    path('profile', profile, name='profile')
]
