from django.db import models

# Create your models here.
class Review(models.Model):
    client_name = models.CharField(max_length=300)
    content = models.TextField()

    def __str__(self):
        return self.client_name
