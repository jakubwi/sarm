from django.contrib import admin
from pages.models import Klasy

class KlasyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tank', 'heal', 'melee', 'ranged')

admin.site.register(Klasy, KlasyAdmin)