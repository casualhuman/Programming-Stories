from django.contrib import admin
from .models import Profile, EmailList


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']


@admin.register(EmailList)
class EmailListAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']