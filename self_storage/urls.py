from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('storage.urls', namespace='storage')),
    path('', include('pages.urls', namespace='pages')),
    path('', include('user.urls', namespace='user')),
]
