from django.contrib import admin
from django import forms
from .widgets import VideoUploadWidget
from .models import Property, PropertyMedia
from .admin_owners import *
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


class PropertyMediaForm(forms.ModelForm):
    class Meta:
        model = PropertyMedia
        fields = '__all__'
        widgets = {
            'file': VideoUploadWidget(),
        }

class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    form = PropertyMediaForm
    extra = 1
    readonly_fields = ("preview",)

    class Media:
        js = ('admin/js/video_upload_progress.js')

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
    fields = (
        "title",
        "owner",
        "description",
        "city_area",
        "property_type",
        "listing_type",
        "price",
        "carpet_area",
        "built_up_area",
        "plot_area",
        "is_available",
    )
    inlines = [PropertyMediaInline]


@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display  = ("property", "media_type")
    list_filter   = ("media_type",)
    search_fields = ("property__title",)



@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'get_user', 'expire_date']
    readonly_fields = ['session_data_decoded']

    def get_user(self, obj):
        data = obj.get_decoded()
        uid = data.get('_auth_user_id')
        if uid:
            try:
                return User.objects.get(pk=uid)
            except User.DoesNotExist:
                return 'Unknown'
        return 'Anonymous'
    get_user.short_description = 'User'

    def session_data_decoded(self, obj):
        return obj.get_decoded()
    session_data_decoded.short_description = 'Session Data'
