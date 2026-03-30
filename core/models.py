from django.db import models
from django.contrib.auth.models import User


class PasswordResetRequest (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField (auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
# Create your models here.


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_active = models.BooleanField(default=False)  # Admin toggles this
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class block_profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)