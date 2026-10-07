from django.db import models
from django.core.validators import MinValueValidator

class Vehicle(models.Model):
    
    VEHICLE_TYPES = [
        ("car","car"),
        ("bike","bike")
    ]
    
    FUEL_TYPES = [
        ("petrol","petrol"),
        ("diesel","diesel"),
        ("electric","electric")
    ]
    
    vehicle_type = models.CharField( max_length=50,choices=VEHICLE_TYPES)
    model_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    fuel_type = models.CharField(max_length=30,choices=FUEL_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    is_sold = models.BooleanField(default=False)
    picture = models.ImageField(upload_to="vehicles/", blank=True, null=True)

    def __str__(self):
        return f"{self.registration_number} - {self.model_name}"


class Sale(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.PROTECT, related_name="sale")
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=30)
    customer_address = models.TextField()
    sold_price = models.DecimalField(max_digits=12, decimal_places=2)
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} sold to {self.customer_name}"
