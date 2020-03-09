from django.db import models

# Create your models here.
class SocialMedia(models.Model):
    facebook= models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    youtube = models.CharField(max_length=255)
