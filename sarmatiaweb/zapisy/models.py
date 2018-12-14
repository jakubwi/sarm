from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta, time
from pytz import timezone
from users.models import UserPostac
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Wymagania(models.Model):
    text = models.TextField(max_length=1024)

    class Meta:
        verbose_name_plural = 'Wymagania'

    def __str__(self):
        return self.text

class EventBlueprint(models.Model):
    nazwaSzablonu = models.CharField(max_length=50)
    nazwaEventu = models.CharField(max_length=50)
    kiedy_godzina = models.TimeField(default=time(20, 00, 00))
    opis = models.TextField(max_length=500)
    miejsca = models.PositiveIntegerField(default=30, blank=True, null=True)
    alty = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nazwaSzablonu

class Event(models.Model):
    nazwa = models.CharField(max_length=50)
    kiedy_dzien = models.DateField()
    kiedy_godzina = models.TimeField(default=time(20, 00, 00))
    opis = models.TextField(max_length=500)
    miejsca = models.PositiveIntegerField(default=30, blank=True, null=True)
    usuniety = models.BooleanField(default=False)
    alty = models.BooleanField(default=False)
    odblokuj_zapisy = models.BooleanField(default=False)

    class Meta:
        ordering = ('kiedy_dzien', 'kiedy_godzina',)

    ## status legend: 1-Otwarte zapisy, 2-Zamrozony, 3-Zakonczony
    def status(self):
        now = datetime.now()
        dzien_godzina = datetime.combine(self.kiedy_dzien, self.kiedy_godzina)
        if now > (dzien_godzina + timedelta(minutes=180)):
            return 3
        elif now >= (dzien_godzina - timedelta(minutes=60)):
            return 2
        else:
            return 1
    
    def __str__(self):
        return self.nazwa + ' ' + str(self.kiedy_dzien)

class Zapis(models.Model):
    kto = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    czym = models.ForeignKey(UserPostac, on_delete=models.CASCADE)
    na_co = models.ForeignKey(Event, on_delete=models.CASCADE)
    wysoka = '3'
    srednia = '2'
    niska = '1'
    gotowosc_choices = ((wysoka, 'Zależy mi na raidzie'), (srednia, 'Mogę iść, mogę nie iść'), (niska, 'Pójdę wyłącznie jeśli będę potrzebny'),)
    gotowosc = models.CharField(max_length=2, choices=gotowosc_choices, default=3,)
    komentarz = models.CharField(max_length=120, null=True, blank=True)
    kiedy = models.DateTimeField(default=datetime.now, blank=True)
    wybrany = models.BooleanField(default=False)
    anulowany = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Zapisy'

    def __str__(self):
        return str(self.czym)