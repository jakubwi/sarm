from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('rekrutacja', views.RekrutacjaListView.as_view(), name='rekrutacja_lista'),
    path('rekrutacja/<int:pk>/update', views.RekrutacjaUpdateView.as_view(), name='rekrutacja_update'),
    path('klasa', views.KlasaListView.as_view(), name='klasa_lista'),
    path('klasa/create', views.KlasaCreateView.as_view(), name='klasa_create'),
    path('klasa/<int:pk>/delete', views.KlasaDeleteView.as_view(), name='klasa_delete'),
    path('rekrutacja/<int:pk>/create', views.RekrutacjaCreateView.as_view(), name='rekrutacja_create'),
    path('killshot', views.KillshotListView.as_view(), name='killshot_lista'),
    path('killshot/create', views.KillshotCreateView.as_view(), name='killshot_create'),
    path('killshot/<int:pk>/delete', views.KillshotDeleteView.as_view(), name='killshot_delete'),
]