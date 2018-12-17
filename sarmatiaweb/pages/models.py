from django.db import models
from datetime import datetime

class Onas(models.Model):
    text = models.TextField(max_length=1024)

    class Meta:
        verbose_name_plural = 'O nas'

    def __str__(self):
        return self.text

class Killshot(models.Model):
    boss = models.CharField(max_length=50, unique=True, default='', null=True, blank=True)
    image = models.ImageField(upload_to='killshots', blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    
    class Meta:
        ordering = ('date',)
    
    def __str__(self):
        return self.boss

class Klasa(models.Model):
    name = models.CharField(max_length=50, unique=True, default='', help_text="Tworząc nową klasę, zaznacz role w polu 'rekrutacja'.", null=True, blank=True)
    icon = models.ImageField(upload_to='class_icons', blank=True)
    tank = models.BooleanField(default=False)
    heal = models.BooleanField(default=False)
    melee = models.BooleanField(default=False)
    ranged = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Klasy'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Rekrutacja(models.Model):
    klasa = models.OneToOneField(Klasa, on_delete=models.CASCADE)
    tank = models.BooleanField(default=False)
    heal = models.BooleanField(default=False)
    melee = models.BooleanField(default=False)
    ranged = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Rekrutacja'
        ordering = ('klasa',)

    def __str__(self):
        return self.klasa.name


