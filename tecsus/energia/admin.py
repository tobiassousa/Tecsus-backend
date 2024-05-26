from django.contrib import admin
from .models import FornecedorEnergia, EnderecoEnergia, FatoContratoEnergia, ClienteContrato


@admin.register(FornecedorEnergia)
class FornecedorEnergiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FornecedorEnergia._meta.fields]


@admin.register(EnderecoEnergia)
class EnderecoEnergiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EnderecoEnergia._meta.fields]


@admin.register(FatoContratoEnergia)
class FatoContratoEnergiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FatoContratoEnergia._meta.fields]


@admin.register(ClienteContrato)
class ClienteContratoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClienteContrato._meta.fields]
    list_filter = ["num_contrato", "num_cliente"]