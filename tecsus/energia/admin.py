from django.contrib import admin

from .models import ContratoEnergia, ProEnergia

@admin.register(ContratoEnergia)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContratoEnergia._meta.fields]

@admin.register(ProEnergia)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProEnergia._meta.fields]