from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "recipient", "verb", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "verb")
    search_fields = ("actor__username", "recipient__username", "verb", "target_id")
    readonly_fields = ("created_at", )
    date_hierarchy = "created_at"
