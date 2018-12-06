from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProgressView.as_view(), name='progress'),
    path('expansion/create', views.ExpansionCreateView.as_view(), name='progress_expansion_create'),
    path('expansion/<int:pk>/update', views.ExpansionUpdateView.as_view(), name='progress_expansion_update'),
    path('raid/create', views.RaidCreateView.as_view(), name='progress_raid_create'),
    path('raid/<int:pk>/update', views.RaidUpdateInlineView, name='progress_raid_update'),
    path('raid/<int:pk>/delete', views.RaidDeleteView.as_view(), name='progress_raid_delete'),
    path('boss/<int:pk>/update', views.BossUpdateView.as_view(), name='progress_boss_update'),
    
]