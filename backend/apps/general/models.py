from django.db import models

from apps.common.models import BaseModel


class Newsletter(BaseModel):
    email = models.EmailField(unique=True)
