from django.db import models


class EventTypeChoices(models.TextChoices):
    # TODO: MIGHT REMOVE SOME LATER TO AVOID COMPLICATING THINGS
    PAGE_VIEW = "page_view", "Page View"
    PAGE_LOAD = "page_load", "Page load"
    SCROLL = "scroll", "Scroll"
    CLICK = "click", "Click"
    SHARE = "share", "Share"
    # REACTION = "reaction", "Reaction"
    # COMMENT = "comment", "Comment"
    # SAVE = "save", "Save"
    SESSION_START = "session_start", "Session Start"
    SESSION_END = "session_end", "Session End"


class DeviceTypeChoices(models.TextChoices):
    MOBILE = "Mobile", "Mobile"
    TABLET = "Tablet", "Tablet"
    DESKTOP = "Desktop", "Desktop"


class ContentTypeChoices(models.TextChoices):
    ARTICLE = "article", "Article"
    JOB = "job", "Job"
    EVENT = "event", "Event"