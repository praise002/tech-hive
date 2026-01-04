from django.db import models


class EventTypeChoices(models.TextChoices):
    PAGE_VIEW = "page_view", "Page View"
    PAGE_LOAD = "page_load", "Page load"
    CLICK = "click", "Click"
    SHARE = "share", "Share"


class DeviceTypeChoices(models.TextChoices):
    MOBILE = "Mobile", "Mobile"
    TABLET = "Tablet", "Tablet"
    DESKTOP = "Desktop", "Desktop"
