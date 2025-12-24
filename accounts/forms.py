from django import forms 
from .models import UserProfile

class UserPreferenences (forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "preferred_city_area",
            "preferred_property_type",
            "max_budget",
        ]
        widgets = {
            "Preferred_city_area": forms.TextInput(attrs={"placeholder": "City / Area"}),
            "max_budget": forms.NumberInput(attrs={"placeholder": "max Budget"}),
        }