from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.RpView.as_view(), name='rp'),
    path('event/<int:pk>/wybierz-sklad', views.RpEventWybierzSkladView, name='rp_event_wybierz'),
    path('event/<int:pk>/detail', views.RpEventDetailView, name='rp_event_detail'),
    path('event/<int:pk>/update', views.RpEventUpdateView.as_view(), name='rp_event_update'),
    path('nowy-event', views.RpEventCreateView.as_view(), name='rp_event_create'),
    path('historia', views.RpHistoriaView.as_view(), name='rp_historia'),
    path('wymagania/<int:pk>', views.RpWymaganiaUpdate.as_view(), name='rp_wymagania'),
]