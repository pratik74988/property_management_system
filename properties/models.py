from django.db import models
from .models_owners import OwnerProfile, PropertyRequest, Partner
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import subprocess, os

# Create your models here.
class Property (models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('3BHK', '3 BHK'),
        ('2BHK', '2 BHK'),
        ('1BHK', '1 BHK'),
        ('1RK', '1 RK'),
        ('SR', 'Single Room'),
        ('RH', 'Row House'),
        ('BG', 'Bungalow'),
        ('PL', 'Plot')
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

    carpet_area = models.FloatField(null=True, blank=True)
    built_up_area = models.FloatField(null=True, blank=True)
    plot_area = models.FloatField(null=True, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def clean(self):
        if self.listing_type== 'sale':
            # 🟢 Plot
            if self.property_type == 'PL':
                if not self.plot_area:
                    raise ValidationError("Plot area is required for plots.")

                # auto-clean extra fields
                self.carpet_area = None
                self.built_up_area = None

            # 🟡 Row House / Bungalow
            elif self.property_type in ['RH', 'BG']:
                if not self.carpet_area:
                    raise ValidationError("Carpet area is required.")
                if not self.built_up_area:
                    raise ValidationError("Built-up area is required.")
                if not self.plot_area:
                    raise ValidationError("Plot area is required.")
            else:
                if not self.carpet_area:
                    raise ValidationError("Carpet area is required.")
                if not self.built_up_area:
                    raise ValidationError("Built-up area is required.")

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
        # if self.media_type == 'video' and self.file:
        #     self.compress_video()
        print("STORAGE TYPE:", type(self.file.storage))
    
    def compress_video(self):
        input_path = self.file.path
        tmp_path = input_path + '_compressed.mp4'
        result = subprocess.run([
            'ffmpeg', '-y',
            '-i', input_path,
            '-vcodec', 'libx264',
            '-crf', '28',
            '-preset', 'fast',
            '-acodec', 'aac',
            '-movflags', '+faststart',  # enables streaming before full download
            tmp_path            
        ], capture_output=True)
        if result.returncode == 0:
            os.replace(tmp_path, input_path)

        else:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)