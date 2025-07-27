import uuid
from datetime import timedelta

from apps.common.models import BaseModel, IsDeletedModel
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class UserRoleChoices(models.TextChoices):
    EDITOR = "editor", "Editor"
    REVIEWER = "reviewer", "Reviewer"
    USER = "user", "User"


class User(AbstractBaseUser, IsDeletedModel, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=255, unique=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    user_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=UserRoleChoices.choices, default=UserRoleChoices.USER
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
            url = "https://res.cloudinary.com/dq0ow9lxw/image/upload/v1732236186/default-image_foxagq.jpg"
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

class SubscriptionPlan(BaseModel):
    PLAN_CHOICES = [
        ("BASIC", "Basic"),
        ("PREMIUM", "Premium"),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, default="BASIC")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.TextField()
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.SET_NULL, 
        null=True
    )
    

