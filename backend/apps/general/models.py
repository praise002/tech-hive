from django.db import models

from apps.common.models import BaseModel


class Newsletter(BaseModel):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.email
    

class About(BaseModel):  # TODO: ONE ABOUT ONLY
    image = models.ImageField(upload_to="about/", null=True, blank=True)
    body = models.TextField()
    
    @property
    def cover_image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Contact(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    content = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"