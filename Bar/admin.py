from django.contrib import admin

from models import BarMan, Category, Product, Config
from django.contrib import admin

class BarManAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Nom", {'fields' : ['name']})
    ]

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "stock")

class ConfigAdmin(admin.ModelAdmin):
    list_display = ("variable", "value")


admin.site.register(BarMan, BarManAdmin)
admin.site.register(Category)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Product, ProductAdmin)
