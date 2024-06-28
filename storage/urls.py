from django.conf.urls.static import static
from django.urls import path

from self_storage import settings
from storage.views import boxes, confirm_box_order, faq, index, order_box, \
    order_consultation, process_consultation, profile, storages

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
    path('order-box/<int:box_id>', order_box, name='order-box')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
