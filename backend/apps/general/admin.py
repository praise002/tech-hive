from apps.general import models
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse


@admin.register(models.SiteDetail)
class SiteDetailAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create()
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                args=(obj.id,),
            )
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email",)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = list_display
