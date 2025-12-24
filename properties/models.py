from django.db import models

# Create your models here.
class Property (models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('3BHK', '3 BHK'),
        ('2BHK', '2 BHK'),
        ('1BHK', '1 BHK'),
        ('1RK', '1 RK'),
        ('SR', 'Single Room'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    city_area = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    rent = models.IntegerField()
    is_available = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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
    file = models.FileField(upload_to="properties/media/")
    media_type = models.CharField(
        max_length=10,
        choices= MEDIA_TYPE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)