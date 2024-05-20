from django.contrib import admin

from .models import AlertaAgua, ContratoAgua, ProAgua

@admin.register(ContratoAgua)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContratoAgua._meta.fields]

@admin.register(ProAgua)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProAgua._meta.fields]
    
@admin.register(AlertaAgua)
class AlertaAguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlertaAgua._meta.fields]