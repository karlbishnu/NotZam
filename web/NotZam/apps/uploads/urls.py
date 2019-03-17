from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^backgrounds/$', views.backgrounds, name='background_upload'),
    url(r'^activates/$', views.activates, name='activates_upload'),
    url(r'^negatives/$', views.negatives, name='negatives_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
