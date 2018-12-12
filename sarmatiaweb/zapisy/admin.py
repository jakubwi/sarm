from django.contrib import admin
from .models import Wymagania, Event, Zapis

class WymaganiaAdmin(admin.ModelAdmin):
    list_display = ('text',)

class ZapisInline(admin.StackedInline):
    model = Zapis

class EventAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kiedy_dzien', 'kiedy_godzina', 'opis', 'miejsca', 'usuniety', 'alty', 'odblokuj_zapisy')
    inlines = [ZapisInline]

class ZapisAdmin(admin.ModelAdmin):
    list_display = ('na_co', 'czym', 'kto', 'gotowosc', 'komentarz', 'kiedy', 'wybrany', 'anulowany')

admin.site.register(Zapis, ZapisAdmin)
admin.site.register(Wymagania, WymaganiaAdmin)
admin.site.register(Event, EventAdmin)