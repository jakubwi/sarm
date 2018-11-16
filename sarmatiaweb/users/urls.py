from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    url(r'^profil/nowe_haslo/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.NoweHasloView.as_view(),name='nowe_haslo'),
    path('profil', views.ProfilView, name='profil'),
    path('profil/<username>/dodaj_postac', views.ProfilDodajPostacView, name='profil_dodaj_postac'),
]