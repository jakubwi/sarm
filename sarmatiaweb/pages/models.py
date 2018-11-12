from django.db import models

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


