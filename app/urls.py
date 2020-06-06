from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    # Url per la homepage
    url(r'^$', views.seleziona_classe, name='seleziona_classe'),
]