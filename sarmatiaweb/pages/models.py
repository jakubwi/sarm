from django.db import models

class Klasa(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tank = models.BooleanField()
    heal = models.BooleanField()
    melee = models.BooleanField()
    ranged = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Klasy'

    def __str__(self):
        return self.name
    
class Rekrutacja(models.Model):
    klasa = models.ForeignKey(Klasa, on_delete=models.CASCADE)
    rekrutacjaTank = models.BooleanField()
    rekrutacjaHeal = models.BooleanField()
    rekrutacjaMelee = models.BooleanField()
    rekrutacjaRanged = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Rekrutacja'

