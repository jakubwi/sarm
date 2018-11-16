from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from django.core.validators import RegexValidator
from pages.models import Klasa
from rejestracja.models import Serwer, Rasa, Rola, Podanie

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    phone = models.CharField(max_length=13, validators=[RegexValidator(regex='[0-9]{9,12}', message='Sprawdź poprawność numeru telefonu', code='Niepoprawny numer telefonu'),])
    battleTag = models.CharField(max_length=20, validators=[RegexValidator(regex='[A-Za-z0-9]+#[0-9]{4,}$', message='Sprawdź poprawność battleTaga', code='Niepoprawny battleTag'),])
    date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name_plural = 'Profile Użytkowników'

    def __unicode__(self):
        return self.user.username

class UserPostac(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    serwer = models.ForeignKey(Serwer, on_delete=models.SET_DEFAULT, null=True, default='', related_name='postacSerwer')
    rasa = models.ForeignKey(Rasa, on_delete=models.SET_DEFAULT, null=True, default='', related_name='postacRasa')
    klasa = models.ForeignKey(Klasa, on_delete=models.SET_DEFAULT, null=True, default='', related_name='postacKlasa')
    mainspec = models.ForeignKey(Rola, on_delete=models.SET_DEFAULT, null=True, default='', related_name='postacMainspec')
    offspec = models.ForeignKey(Rola, on_delete=models.SET_DEFAULT, null=True, default='', related_name='postacOffspec')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Postacie Userów'
    
    def __str__(self):
        return self.name