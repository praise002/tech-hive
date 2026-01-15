import secrets

from apps.common.models import BaseModel
from django.core.validators import URLValidator
from django.db import models


class Newsletter(BaseModel):
    email = models.EmailField(unique=True)
    unsubscribe_token = models.CharField(max_length=64, unique=True, editable=False)
    is_subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            self.unsubscribe_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def get_unsubscribe_url(self, request=None):
        from django.conf import settings

        return f"{settings.FRONTEND_URL}/newsletter/unsubscribe?token={self.unsubscribe_token}"

    def __str__(self):
        return self.email


class SiteDetail(BaseModel):
    image = models.ImageField(upload_to="about/", null=True, blank=True)
    body = models.TextField()
    fb = models.CharField(max_length=250, validators=[URLValidator()])
    ln = models.CharField(max_length=250, validators=[URLValidator()])
    x = models.CharField(max_length=250, validators=[URLValidator()])
    ig = models.CharField(max_length=250, validators=[URLValidator()])

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Contact(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
