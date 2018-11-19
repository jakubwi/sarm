import django_filters
from django.db import models
from django import forms
from .models import Podanie

CHOICES = (
    ('1','Zaakceptowane'),
    ('0','Odrzucone'),
)

class AplikacjeZamknieteFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nick w podaniu')
    accepted = django_filters.ChoiceFilter(choices=CHOICES, label='Wybierz status podania')
    
    class Meta:
        model = Podanie
        fields = ['name', 'accepted']
