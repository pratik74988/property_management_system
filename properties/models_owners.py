from django.db import models
from django.contrib.auth.models import User


# ─────────────────────────────────────────────
#  Owner profile – assigned on owner sign-up
# ─────────────────────────────────────────────
class OwnerProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owner_profile")
    phone      = models.CharField(max_length=15, blank=True)
    is_approved = models.BooleanField(default=True)   # auto-approved; flip to False if you want manual vetting
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Owner: {self.user.username}"

# ─────────────────────────────────────────────
#  Property listing REQUEST  (not yet published)
# ─────────────────────────────────────────────
class PropertyRequest(models.Model):
    STATUS_CHOICES = [
        ("pending",  "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('3BHK', '3 BHK'),
        ('2BHK', '2 BHK'),
        ('1BHK', '1 BHK'),
        ('1RK',  '1 RK'),
        ('SR',   'Single Room'),
    ]
    LISTING_TYPE_CHOICES = [
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ]

    owner         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="property_requests")
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    city_area     = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    listing_type  = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default="rent")
    price         = models.IntegerField(help_text="Monthly rent or sale price in ₹")
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    submitted_at  = models.DateTimeField(auto_now_add=True)
    reviewed_at   = models.DateTimeField(null=True, blank=True)
    admin_note    = models.TextField(blank=True, help_text="Optional note from admin to owner")

    def __str__(self):
        return f"{self.title} — {self.owner.username} [{self.status}]"

    class Meta:
        ordering = ["-submitted_at"]


# ─────────────────────────────────────────────
#  Partner  (logo-only, shown on /partners/)
# ─────────────────────────────────────────────
class Partner(models.Model):
    name       = models.CharField(max_length=100)
    logo       = models.ImageField(upload_to="partners/")
    is_active  = models.BooleanField(default=True)
    order      = models.PositiveIntegerField(default=0, help_text="Lower number → shown first")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]

class PropertyRequestMedia(models.Model):
    IMAGE = "image"

    MEDIA_TYPE_CHOICES = [
        (IMAGE, "Image"),
    ]

    property_request = models.ForeignKey(
        PropertyRequest,
        related_name="media",
        on_delete=models.CASCADE
    )

    file = models.FileField(upload_to="property_requests/")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default=IMAGE)

    def __str__(self):
        return f"{self.property_request.title} - {self.media_type}"