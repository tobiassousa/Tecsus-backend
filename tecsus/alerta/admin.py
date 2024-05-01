from django.contrib import admin

from .models import AlertaAgua

@admin.register(AlertaAgua)
class AlertaAguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlertaAgua._meta.fields]
