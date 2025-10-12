import logging
from pathlib import Path

from apps.accounts.models import User
from django.conf import settings
from django.db import transaction

logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent


class CreateData:
    def __init__(self):
        with transaction.atomic():
            self.create_superuser()

    def create_superuser(self) -> User:
        user_dict = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": settings.SUPERUSER_EMAIL,
            "password": settings.SUPERUSER_PASSWORD,
            "is_email_verified": True,
        }
        superuser = User.objects.get_or_none(email=user_dict["email"])

        if not superuser:
            superuser = User.objects.create_superuser(**user_dict)

        return superuser
