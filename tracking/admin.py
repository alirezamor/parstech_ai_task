from django.contrib import admin

# Register your models here.
from .models import Shipment, Article


class ShipmentAmin(admin.ModelAdmin):
    list_display = ("tracking_number", "carrier", "receiver_address", "status")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("shipment", "name")


admin.site.register(Shipment, ShipmentAmin)
admin.site.register(Article, ArticleAdmin)
