from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('o-gildii', views.OnasView.as_view(), name='onas'),
    path('o-gildii/<int:pk>', views.OnasUpdateView.as_view(), name='onas_update'),
    path('rekrutacja', views.RekrutacjaUpdateView, name='rekrutacja_update'),
    path('klasa', views.KlasaListView.as_view(), name='klasa_lista'),
    path('klasa/create', views.KlasaCreateView.as_view(), name='klasa_create'),
    path('klasa/<int:pk>/delete', views.KlasaDeleteView.as_view(), name='klasa_delete'),
    path('rekrutacja/<int:pk>/create', views.RekrutacjaCreateView.as_view(), name='rekrutacja_create'),
    path('killshot', views.KillshotListView.as_view(), name='killshot_lista'),
    path('killshot/create', views.KillshotCreateView.as_view(), name='killshot_create'),
    path('killshot/<int:pk>/delete', views.KillshotDeleteView.as_view(), name='killshot_delete'),
]