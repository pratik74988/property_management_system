from django.contrib import admin
from .models import PasswordResetRequest
# Register your models here.



@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin (admin.ModelAdmin):
    list_display = ("user", "created_at", "is_resolved")
    list_filter = ("is_resolved",)
    search_fields = ("user__username",)