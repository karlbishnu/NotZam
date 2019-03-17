from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^model-summary$', views.model_summary, name='ml_model_summary'),
    url(r'^training$', views.training, name='ml_training'),
    url(r'^trigger-word$', views.trigger_word, name='ml_detect_trigger_word'),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
