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
    path('mod/podanie/<int:pk>/detail', views.AplikacjaDetailView, name='aplikacja_detail'),
    path('mod/podanie/<int:pk>/detail/<int:kpk>/delete', views.AplikacjaDeleteKomentarz, name='aplikacja_delete_komentarz'),
    path('mod/podanie/<int:pk>/akceptacja', views.AplikacjaConfirm, name='aplikacja_confirm'),
    path('mod/podanie/<int:pk>/akceptacja/<username>', views.AplikacjaConfirm2, name='aplikacja_confirm2'),
    path('mod/podanie/<int:pk>/akceptacja/<username>/profil', views.AplikacjaConfirm3, name='aplikacja_confirm3'),
    path('mod/podanie/koniec', views.AplikacjaConfirm4.as_view(), name='aplikacja_confirm4'),
    path('moderatorzy/wybierz', views.ModWybierzView.as_view(), name='mod_wybierz'),
    path('moderatorzy/<int:pk>/zmien', views.ModChangeView.as_view(), name='mod_change'),
    path('moderatorzy/lista', views.ModListView.as_view(), name='mod_lista'),
    path('mod/podanie/zakceptowane', views.PodaniaZaakceptowane, name='aplikacje_accepted'),
    ]