"""
app URLs

"""
import importlib

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from common.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

# Auto import urls from custom apps
# Define patterns in the apps
# urls.py in apps must not be empty if present
CUSTOM_APPS = getattr(settings, 'CUSTOM_APPS', [])
urlpatterns += [
    path('', include(app_name + '.urls'))
    for app_name in CUSTOM_APPS
    if importlib.util.find_spec(app_name + '.urls')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
