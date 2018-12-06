from django.contrib import admin
from .models import Raid, Boss, Expansion

class RaidInline(admin.StackedInline):
    model = Raid

class ExpansionAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    inlines = [RaidInline]

class BossAdmin(admin.ModelAdmin):
    list_display = ('raid', 'name', 'mythic', 'heroic', 'normal')

class BossInline(admin.StackedInline):
    model = Boss

class RaidAdmin(admin.ModelAdmin):
    list_display = ('name', 'expansion', 'position', 'aktualny')
    inlines = [BossInline]

admin.site.register(Expansion, ExpansionAdmin)
admin.site.register(Raid, RaidAdmin)
admin.site.register(Boss, BossAdmin)
