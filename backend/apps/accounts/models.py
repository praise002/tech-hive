import random
import uuid
from datetime import timedelta

from apps.common.models import IsDeletedModel
from apps.common.validators import validate_file_size
from apps.content.choices import CURSOR_COLORS
from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


def slugify_two_fields(self):
    return f"{self.first_name}-{self.last_name}"


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = AutoSlugField(
        populate_from=slugify_two_fields, unique=True, always_update=True
    )
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, unique=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Django's authentication gate. Keep True to allow custom account status "
            "checks in views. If False, Django blocks authentication before our custom "
            "logic runs, preventing granular error messages. We manage account access "
            "through is_email_verified, user_active, and is_suspended instead."
        ),
    )
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    is_suspended = models.BooleanField(
        default=False,
        help_text=(
            "Admin suspension flag. When True, account is suspended by staff for "
            "policy violations. Takes priority over user_active. User cannot self-reactivate. "
            "Check this AFTER email verification but BEFORE user_active. "
            "If True, show suspension reason and support contact."
        ),
    )
    mentions_disabled = models.BooleanField(default=False)

    suspended_at = models.DateTimeField(null=True, blank=True)
    suspended_by = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="suspended_users"
    )
    suspension_reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, validators=[validate_file_size]
    )

    cursor_color = models.CharField(
        max_length=7,
        default=random.choice(CURSOR_COLORS),
        help_text="Hex color for Liveblocks cursor and mentions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        ordering = ["-created_at"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    @property
    def avatar_url(self):
        try:
            url = self.avatar.url
        except:
            # url = "https://res.cloudinary.com/dq0ow9lxw/image/upload/v1732236186/default-image_foxagq.jpg"
            url = "https://res.cloudinary.com/dq0ow9lxw/image/upload/v1762111366/Avatars_fpmuzf.png"
        return url


class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.otp)

    @property
    def is_valid(self):
        expiration_time = self.created_at + timedelta(
            minutes=settings.EMAIL_OTP_EXPIRE_MINUTES
        )
        return timezone.now() < expiration_time


class ContributorOnboarding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    terms_accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(auto_now_add=True)
