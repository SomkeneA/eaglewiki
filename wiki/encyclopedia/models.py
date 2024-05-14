from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Add other fields as needed


class Entry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title