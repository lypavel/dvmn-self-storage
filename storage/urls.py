from django.urls import path

from storage.views import boxes, faq, index, order_consultation, \
    process_consultation, profile, storages

app_name = 'storage'

urlpatterns = [
    path('', index, name='index'),
    path('faq', faq, name='faq'),
    path('storages', storages, name='storages'),
    path('boxes/<int:storage_id>', boxes, name='boxes'),
    path('profile', profile, name='profile'),
    path('order-consultation', order_consultation, name='order-consultation'),
    path(
        'process-consultation',
        process_consultation,
        name='process-consultation'
    ),
]
