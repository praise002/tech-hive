from django.contrib import admin

from apps.general import models

@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    pass

@admin.register(models.About)
class AboutAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    pass