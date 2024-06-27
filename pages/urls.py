from django.urls import path

from .views import tariffs, reviews, contacts

app_name = 'pages'

urlpatterns = [
    path('tariffs', tariffs, name='tariffs'),
    path('reviews', reviews, name='reviews'),
    path('contacts', contacts, name='contacts'),
]
