from django.urls import path

from storage.views import boxes, faq, index, order_box, \
    order_consultation, process_consultation, profile, send_qr, storages

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
    path('order-box/<int:box_id>', order_box, name='order-box'),
    path('send_qr', send_qr, name='send_qr'),

    path('email-confirm/<str:user_verified>',
         index,
         name='index_user_verified'),
    path('user-registered/<str:after_registration>',
         index,
         name='index_after_registration'),
]
