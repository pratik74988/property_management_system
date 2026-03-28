from django.db import models
from .models_owners import OwnerProfile, PropertyRequest, Partner
from django.contrib.auth.models import User
# Create your models here.
class Property (models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('3BHK', '3 BHK'),
        ('2BHK', '2 BHK'),
        ('1BHK', '1 BHK'),
        ('1RK', '1 RK'),
        ('SR', 'Single Room'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    LISTING_TYPE_CHOICES = [
        ('rent', 'for Rent'),
        ('sale', 'for sale'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    city_area = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='rent')  # ← ADD THIS
    price = models.IntegerField(help_text="Monthly rent or Sale Price in rs")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()})"

class PropertyMedia(models.Model):
    IMAGE = "image"
    VIDEO = "video"
    MEDIA_TYPE_CHOICES = [
        (IMAGE, "image"),
        (VIDEO, "video"),
    ]
    property = models.ForeignKey(
        Property,
        related_name="media",
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="properties/")
    media_type = models.CharField(
        max_length=10,
        choices= MEDIA_TYPE_CHOICES
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("STORAGE TYPE:", type(self.file.storage))