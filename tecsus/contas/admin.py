from django.contrib import admin
from .models import Agua, Energia, Gas

@admin.register(Agua)
class AguaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Agua._meta.fields]

@admin.register(Energia)
class EnergiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Energia._meta.fields]

@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Gas._meta.fields]
