from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('3BHK', '3 BHK'),
        ('2BHK', '2 BHK'),
        ('1BHK', '1 BHK'),
        ('1RK', '1 RK'),
        ('SR', 'Single Room'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_city_area = models.CharField(max_length=100, blank=True)
    preferred_property_type = models.CharField(
        max_length=10, choices=PROPERTY_TYPE_CHOICES, blank=True
    )
    max_budget = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username
