from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from datetime import datetime
from django.contrib.auth.models import User
from pages.models import Klasa

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='Usunięty')[0]

def get_sentinel_serwer():
    return Serwer.objects.get_or_create(name='Usunięty')[0]

class Serwer(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Serwery'
    
    def __str__(self):
        return self.name

class Rasa(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Rasy'
    
    def __str__(self):
        return self.name

class Rola(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Role'
    
    def __str__(self):
        return self.name

class Podanie(models.Model):
    name = models.CharField(max_length=20)
    serwer = models.ForeignKey(Serwer, on_delete=models.SET(get_sentinel_serwer), default='')
    rasa = models.ForeignKey(Rasa, on_delete=models.SET_DEFAULT, null=True, default='')
    klasa = models.ForeignKey(Klasa, on_delete=models.SET_DEFAULT, null=True, default='')
    mainspec = models.ForeignKey(Rola, on_delete=models.SET_DEFAULT, null=True, related_name='mainspec', default='')
    offspec = models.ForeignKey(Rola, on_delete=models.SET_DEFAULT, null=True, related_name='offspec', default='')
    infoRaidDoswiadczenie = models.TextField(max_length=700, blank=True)
    infoRaidWiedza = models.TextField(max_length=700, blank=True)
    infoRaidDni = models.TextField(max_length=700, blank=True)
    infoGildie = models.TextField(max_length=700)
    infoOgolne = models.TextField(max_length=700)
    K = 'K'
    M = 'M'
    N = '-'
    plec_choices = ((K, 'K'), (M, 'M'), (N, '-'),)
    plec = models.CharField(
        max_length=2,
        choices=plec_choices, null=True, blank=True,
    )
    battleTag = models.CharField(max_length=20, validators=[RegexValidator(regex='[A-Za-z0-9]+#[0-9]{4,}$', message='Sprawdź poprawność battleTaga', code='Niepoprawny battleTag'),])
    email = models.EmailField(max_length=125)
    emailConfirm = models.EmailField(max_length=125)
    date = models.DateTimeField(default=datetime.now, blank=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Podania'
        ordering = ('name',)

    def __str__(self):
        return self.name

class PodanieKomentarze(models.Model):
    podanie = models.ForeignKey(Podanie, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), default='')
    comment = models.TextField(max_length=1024)
    date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name_plural = 'PodanieKomentarze'
        ordering = ('-date',)

    def __unicode__(self):
        return self.comment