from django.contrib import admin
from .models import Property, PropertyMedia
from .admin_owners import *
from django.utils.html import mark_safe

class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 0
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" width="100" />')
        return "No Image"

    preview.short_description = "Preview"

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "city_area",
        "property_type",
        "listing_type",   # ← new
        "price",
        "is_available",
        "created_at",
    )

    list_filter = (
        "listing_type",   # ← new — filter sidebar: For Rent / For Sale
        "city_area",
        "property_type",
        "is_available",
        "owner",
    )

    search_fields = (
        "title",
        "city_area",
        "description",
    )

    ordering = ("-created_at",)
    inlines = [PropertyMediaInline]


@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display  = ("property", "media_type")
    list_filter   = ("media_type",)
    search_fields = ("property__title",)


