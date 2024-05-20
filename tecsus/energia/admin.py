from django.contrib import admin

from .models import AlertaEnergia, ContratoEnergia, ProEnergia

@admin.register(ContratoEnergia)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContratoEnergia._meta.fields]

@admin.register(ProEnergia)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProEnergia._meta.fields]
    list_filter = ["num_cliente", "num_contrato"]
    
@admin.register(AlertaEnergia)
class AlertaEnergiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AlertaEnergia._meta.fields]
