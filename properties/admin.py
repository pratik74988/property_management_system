from django.contrib import admin
from .models import Property
# Register your models here.

from django.contrib import admin
from .models import Property, PropertyMedia  


class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city_area",
        "property_type",
        "rent",
        "is_available",
        "created_at",
    )

    list_filter = (
        "city_area",
        "property_type",
        "is_available",
    )

    search_fields = (
        "title",
        "city_area",
        "description",
    )

    ordering = ("-created_at",)
    inlines = [PropertyMediaInline] 