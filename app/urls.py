from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    # Url per la homepage
    path('', views.seleziona_classe, name='seleziona_classe'),
    # Url per la pagina di votazione delle classi
    path('vota/<pk>/', views.vota, name='vota'),
    # Url per la fine
    path('fine/', views.fine, name='fine'),

    # Urls per il sistema di autenticazione
    path('', include('social.apps.django_app.urls', namespace='social')),
    path('logout/', views.logout, name='logout')
]