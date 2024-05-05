from django.contrib import admin

from .models import AlertaAgua, AlertaEnergia

@admin.register(AlertaAgua)
class AlertaAguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlertaAgua._meta.fields]
    

@admin.register(AlertaEnergia)
class AlertaEnergiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlertaEnergia._meta.fields]
