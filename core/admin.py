from django.contrib import admin
from .models import PasswordResetRequest, Announcement, block_profiles
# Register your models here.



@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin (admin.ModelAdmin):
    list_display = ("user", "created_at", "is_resolved")
    list_filter = ("is_resolved",)
    search_fields = ("user__username",)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_editable = ['is_active']   # Toggle directly from the list view
    search_fields = ['title']


admin.site.register(block_profiles)