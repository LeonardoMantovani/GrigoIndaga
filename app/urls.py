from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    # Url per la homepage
    path('', views.seleziona_classe, name='seleziona_classe'),
    # Url per la pagina di votazione delle classi
    path('vota/<pk>/', views.vota, name='vota'),
    # Url per la fine
    path('fine/', views.fine, name='fine'),
]