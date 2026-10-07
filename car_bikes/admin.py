from django.contrib import admin
from .models import Sale, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "model_name", "vehicle_type", "price", "is_sold")
    list_filter = ("vehicle_type", "fuel_type")
    search_fields = ("registration_number", "model_name")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "customer_name", "customer_phone", "sold_price", "sold_at")
    search_fields = ("vehicle__registration_number", "customer_name", "customer_phone")
