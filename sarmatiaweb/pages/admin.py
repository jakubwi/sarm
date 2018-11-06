from django.contrib import admin
from pages.models import Klasa, Rekrutacja

class KlasaAdmin(admin.ModelAdmin):
    list_display = ('name', 'tank', 'heal', 'melee', 'ranged')

class RekrutacjaAdmin(admin.ModelAdmin):
    list_display = ('klasa', 'rekrutacjaTank', 'rekrutacjaHeal', 'rekrutacjaMelee', 'rekrutacjaRanged',)

admin.site.register(Klasa, KlasaAdmin)
admin.site.register(Rekrutacja, RekrutacjaAdmin)