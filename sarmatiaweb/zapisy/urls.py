from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.RpView, name='rp'),
    #path('', views.RpView.as_view(), name='rp'),
    path('event/<int:pk>/wybierz-sklad', views.RpEventWybierzSkladView, name='rp_event_wybierz'),
    path('event/<int:pk>/detail', views.RpEventDetailView, name='rp_event_detail'),
    path('event/<int:pk>/update', views.RpEventUpdateView.as_view(), name='rp_event_update'),
    path('nowy-event', views.RpEventNewView, name='rp_event_new'),
    path('nowy-event/<int:pk>/', views.RpEventCreateFromBlueprintView, name='rp_event_create_from_blueprint'),
    path('nowy-event-jednorazowy', views.RpEventCreateView.as_view(), name='rp_event_create'),
    path('nowy-szablon', views.RpEventBlueprintCreateView.as_view(), name='rp_event_blueprint_create'),
    path('historia', views.RpHistoriaView.as_view(), name='rp_historia'),
    path('wymagania/<int:pk>', views.RpWymaganiaUpdate.as_view(), name='rp_wymagania'),
]