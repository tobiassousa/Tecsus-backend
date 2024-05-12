from django.contrib import admin

import agua.models as agua


@admin.register(agua.FornecedorAgua)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in agua.FornecedorAgua._meta.fields]


@admin.register(agua.Endereco)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in agua.Endereco._meta.fields]


@admin.register(agua.FatoContratoAgua)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in agua.FatoContratoAgua._meta.fields]