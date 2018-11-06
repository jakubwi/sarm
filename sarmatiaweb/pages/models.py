from django.db import models

class Klasy(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tank = models.BooleanField()
    heal = models.BooleanField()
    melee = models.BooleanField()
    ranged = models.BooleanField()
    
