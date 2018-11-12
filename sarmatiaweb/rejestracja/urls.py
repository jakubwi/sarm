from django.urls import path
from . import views

urlpatterns = [
    path('mod', views.PanelModaView, name='panel_moda'),
    path('serwer/nowy', views.SerwerCreateView.as_view(), name='serwer_create'),
    path('serwer', views.SerwerListView.as_view(), name='serwer_lista'),
    path('serwer/<int:pk>/delete', views.SerwerDeleteView.as_view(), name='serwer_delete'),
    path('rasa/nowa', views.RasaCreateView.as_view(), name='rasa_create'),
    path('rasa', views.RasaListView.as_view(), name='rasa_lista'),
    path('rasa/<int:pk>/delete', views.RasaDeleteView.as_view(), name='rasa_delete'),
    path('rola/nowa', views.RolaCreateView.as_view(), name='rola_create'),
    path('rola', views.RolaListView.as_view(), name='rola_lista'),
    path('rola/<int:pk>/delete', views.RolaDeleteView.as_view(), name='rola_delete'),
    path('aplikacja', views.AplikacjaView.as_view(), name='aplikacja'),
    path('aplikacja/raid', views.AplikacjaRaidView.as_view(), name='aplikacja_raid'),
    path('aplikacja/social', views.AplikacjaSocialView.as_view(), name='aplikacja_social'),
    path('mod/podanie/<int:pk>/detail', views.PodanieDetailView, name='podanie_detail'),
]