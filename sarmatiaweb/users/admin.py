from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserProfile, UserPostac

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', ]
    model = CustomUser

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'battleTag', 'date']

class UserPostacAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'serwer', 'rasa', 'klasa', 'mainspec', 'offspec', 'is_main']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserPostac, UserPostacAdmin)