from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models_owners import PropertyRequest


# ─────────────────────────────────────────────
#  Owner Sign-Up Form
# ─────────────────────────────────────────────
class OwnerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")
    phone = forms.CharField(max_length=15, required=False, label="Phone number (optional)")

    class Meta:
        model  = User
        fields = ("username", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            from .models_owners import OwnerProfile
            OwnerProfile.objects.create(
                user  = user,
                phone = self.cleaned_data.get("phone", ""),
            )
        return user


# ─────────────────────────────────────────────
#  Property Listing Request Form  (for owners)
# ─────────────────────────────────────────────
class PropertyRequestForm(forms.ModelForm):
    class Meta:
        model  = PropertyRequest
        fields = (
            "title",
            "description",
            "city_area",
            "property_type",
            "listing_type",
            "price",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "city_area": "City / Area",
            "price":     "Rent / Sale Price (₹)",
        }