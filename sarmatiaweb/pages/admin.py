from django.contrib import admin
from pages.models import Klasa, Rekrutacja, Killshot

class KillshotAdmin(admin.ModelAdmin):
    list_display = ('boss', 'image', 'date')

class RekrutacjaInline(admin.StackedInline):
    model = Rekrutacja

class KlasaAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'tank', 'heal', 'melee', 'ranged')
    inlines = [RekrutacjaInline]

class RekrutacjaAdmin(admin.ModelAdmin):
    list_display = ('klasa', 'tank', 'heal', 'melee', 'ranged')

admin.site.register(Killshot, KillshotAdmin)
admin.site.register(Klasa, KlasaAdmin)
admin.site.register(Rekrutacja, RekrutacjaAdmin)