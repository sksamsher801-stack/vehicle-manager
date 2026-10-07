from django import forms
from .models import Sale, Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "vehicle_type",
            "model_name",
            "registration_number",
            "fuel_type",
            "price",
            "picture",
        ]

    def clean_registration_number(self):
        return self.cleaned_data["registration_number"].strip().upper()
        
    def clean_model_name(self):
        model_name = self.cleaned_data["model_name"].strip()
        if not model_name:
            raise forms.ValidationError("Model name cant not be empty...")
        return model_name
    
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["customer_name", "customer_phone", "customer_address"]
