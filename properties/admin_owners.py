from django.contrib import admin
from django.utils import timezone
from .models_owners import OwnerProfile, PropertyRequest, Partner, PropertyRequestMedia
from .models import Property, PropertyMedia   # existing
from django.utils.html import mark_safe
# ─────────────────────────────────────────────
#  Owner Profile
# ─────────────────────────────────────────────
class PropertyRequestMediaInline(admin.TabularInline):
    model = PropertyRequestMedia
    extra = 0
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" width="100" />')
        return "No Image"
    
@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display  = ("user", "phone", "is_approved", "created_at")
    list_filter   = ("is_approved",)
    search_fields = ("user__username", "user__email", "phone")


# ─────────────────────────────────────────────
#  Property Request  — approve / reject action
# ─────────────────────────────────────────────
@admin.action(description="✅ Approve selected requests and publish properties")
def approve_requests(modeladmin, request, queryset):
    from django.contrib import messages

    count = 0

    for req in queryset:
        try:
            # Create Property
            property_obj = Property.objects.create(
                owner=req.owner,
                title=req.title,
                description=req.description,
                city_area=req.city_area,
                property_type=req.property_type,
                listing_type=req.listing_type,
                price=req.price,
                is_available=True,
            )

            # Copy Images
            for media in req.media.all():
                PropertyMedia.objects.create(
                    property=property_obj,
                    file=media.file,
                    media_type="image"
                )

            # Mark approved
            req.status = "approved"
            req.reviewed_at = timezone.now()
            req.save()

            count += 1

        except Exception as e:
            messages.error(request, f"Error approving {req.title}: {e}")

    messages.success(request, f"{count} properties approved successfully!")

@admin.action(description="❌ Reject selected requests")
def reject_requests(modeladmin, request, queryset):
    queryset.filter(status="pending").update(
        status      = "rejected",
        reviewed_at = timezone.now(),
    )


@admin.register(PropertyRequest)
class PropertyRequestAdmin(admin.ModelAdmin):
    list_display  = ("title", "owner", "listing_type", "property_type", "price", "status", "submitted_at")
    list_filter   = ("status", "listing_type", "property_type")
    search_fields = ("title", "owner__username", "city_area")
    readonly_fields = ("submitted_at", "reviewed_at", "owner")
    actions       = [approve_requests, reject_requests]

    inlines = [PropertyRequestMediaInline]
    fieldsets = (
        ("Submission Info", {
            "fields": ("owner", "submitted_at", "status", "reviewed_at", "admin_note")
        }),
        ("Property Details", {
            "fields": ("title", "description", "city_area", "property_type", "listing_type", "price")
        }),
    )


# ─────────────────────────────────────────────
#  Partners
# ─────────────────────────────────────────────
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display  = ("name", "is_active", "order", "created_at")
    list_editable = ("is_active", "order")
    search_fields = ("name",)