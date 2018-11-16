from django.contrib import admin
from rejestracja.models import Serwer, Rasa, Rola, Podanie, PodanieKomentarze



class SerwerAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RasaAdmin(admin.ModelAdmin):
    list_display = ('name',)

class RolaAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PodanieRaidAdmin(admin.ModelAdmin):
    list_display = ['name',
                'accepted',
                'rejected',
                'date',
                'serwer',
                'rasa', 
                'klasa',
                'mainspec',
                'offspec',
                'battleTag',
                'email',
                'emailConfirm',
        ]

class PodanieKomentarzeAdmin(admin.ModelAdmin):
    list_display = ['podanie', 'author', 'date']

admin.site.register(Serwer, SerwerAdmin)
admin.site.register(Rasa, RasaAdmin)
admin.site.register(Rola, RolaAdmin)
admin.site.register(Podanie, PodanieRaidAdmin)
admin.site.register(PodanieKomentarze, PodanieKomentarzeAdmin)