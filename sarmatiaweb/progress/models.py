from django.db import models

class Expansion(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    position = models.PositiveIntegerField(blank=True, null=True, help_text="0-Vanilla, 1-TBC, 2-WotLK, 3-Cata, 4-MoP, 5-WoD, 6-Legion, 7-BfA, itd.", )
    aktualny = models.BooleanField(default=False, help_text="Zaznacz, jeśli ten dodatek jest aktualnie progressowany",)

    class Meta:
        verbose_name_plural = 'Expansions'
        ordering = ('position',)

    def __str__(self):
        return self.name

class Raid(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    expansion = models.ForeignKey(Expansion, on_delete=models.CASCADE, null=True, default='', related_name='raids')
    position = models.PositiveIntegerField(blank=True, null=True, help_text="Wpisz cyfrę odpowiadającą kolejności progressu")
    aktualny = models.BooleanField(default=False, help_text="Zaznacz, jeśli raid jest aktualnie progresowany",)
    
    class Meta:
        verbose_name_plural = 'Raids'
        ordering = ('position',)

    def __str__(self):
        return self.name

class Boss(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    raid = models.ForeignKey(Raid, on_delete=models.CASCADE, null=True, default='', related_name='bosses')
    mythic = models.BooleanField(default=False)
    heroic = models.BooleanField(default=False)
    normal = models.BooleanField(default=False)
    position = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Boss'
        ordering = ('position',)

    def __str__(self):
        return self.name