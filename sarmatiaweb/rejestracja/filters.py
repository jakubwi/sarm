import django_filters
from django.db import models
from django import forms
from .models import Podanie, PodanieKomentarze
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.db.models import Count
from django.db.models import Q

class CustomOrderingFilter(django_filters.OrderingFilter):

    def __init__(self, *args, **kwargs):
        super(CustomOrderingFilter, self).__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('comments', 'Komentarze (od: najwięcej)'), 
            ('-comments', 'Komentarze (od: najmniej)'),
            ('date', 'Data (od najstarszych)'),
            ('-date', 'Data (od najnowszych)'),
            ('name', 'Nazwa postaci (od A do Z)'),
            ('-name', 'Nazwa postaci (od Z do A)'),
            ]


    def filter(self, qs, value):
        # OrderingFilter is CSV-based, so `value` is a list
        if any(v in ['comments'] for v in value):
            queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & (Q(accepted=True) | Q(rejected=True))).order_by('-num_comm')
            return queryset
        elif any(v in ['-comments'] for v in value):
            queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & (Q(accepted=True) | Q(rejected=True))).order_by('num_comm')
            return queryset

        return super(CustomOrderingFilter, self).filter(qs, value)

CHOICES = (
    ('1','Zaakceptowane'),
    ('0','Odrzucone'),
)

class AplikacjeZamknieteFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nazwa postaci')
    accepted = django_filters.ChoiceFilter(choices=CHOICES, label='Status podania')
    start_date = django_filters.DateTimeFilter(field_name='date', label='Data: od', lookup_expr='gte', widget=DateTimePickerInput(format='%Y-%m-%d %H:%M:%S'))
    end_date = django_filters.DateTimeFilter(field_name='date', label='Data: do', lookup_expr='lte', widget=DateTimePickerInput(format='%Y-%m-%d %H:%M:%S'))
    #number_of_comments = django_filters.ChoiceFilter(queryset=Podanie.objects.annotate(num_comm=Count('comments')).filter(num_comm__gte=1))

    o = CustomOrderingFilter()

    class Meta:
        model = Podanie
        fields = ['name', 'accepted', ]