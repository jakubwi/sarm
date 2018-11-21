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
            ('date', 'Data (od najstarszych)'),
            ('-date', 'Data (od najnowszych)'),
            ('name', 'Nazwa postaci (od A do Z)'),
            ('-name', 'Nazwa postaci (od Z do A)'),
            ('comments', 'Komentarze: wszystko (od: najwięcej)'), 
            ('-comments', 'Komentarze: wszystko (od: najmniej)'),
            ('commentsZ', 'Komentarze w zaakceptowanych (od: najwięcej)'), 
            ('-commentsZ', 'Komentarze w zaakceptowanych (od: najmniej)'),
            ('commentsO', 'Komentarze w odrzuconych (od: najwięcej)'),
            ('-commentsO', 'Komentarze w odrzuconych (od: najmniej)'),
            ]

    def filter(self, qs, value):
        if value:
            if any(v in ['commentsZ'] for v in value):
                queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & Q(accepted=True)).order_by('-num_comm')
                return queryset
            elif any(v in ['-commentsZ'] for v in value):
                queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & Q(accepted=True)).order_by('num_comm')
                return queryset
            elif any(v in ['commentsO'] for v in value):
                queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & Q(rejected=True)).order_by('-num_comm')
                return queryset
            elif any(v in ['-commentsO'] for v in value):
                queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & Q(rejected=True)).order_by('num_comm')
                return queryset
            elif any(v in ['comments'] for v in value):
                queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & (Q(accepted=True) | Q(rejected=True))).order_by('-num_comm')
                return queryset
            elif any(v in ['-comments'] for v in value):
                queryset = Podanie.objects.annotate(num_comm=Count('comments')).filter(Q(num_comm__gte=1) & (Q(accepted=True) | Q(rejected=True))).order_by('num_comm')
                return queryset
        else:
            return super(CustomOrderingFilter, self).filter(qs, value)
        
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

    o = CustomOrderingFilter()

    class Meta:
        model = Podanie
        fields = ['name', 'accepted', ]