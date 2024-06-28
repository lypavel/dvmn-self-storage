from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from self_storage import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('storage.urls', namespace='storage')),
                  path('', include('pages.urls', namespace='pages')),
                  path('', include('user.urls', namespace='user')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
