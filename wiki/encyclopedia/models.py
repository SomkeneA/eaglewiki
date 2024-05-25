from django.conf import settings
from django.db import models
from PIL import Image
from django.contrib.auth.models import User
import os

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Add other fields as needed


class Entry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        if self.image and not self.thumbnail:
            image = Image.open(self.image.path)
            image.thumbnail((200, 200), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
            thumbnail_name, thumbnail_extension = os.path.splitext(self.image.name)
            thumbnail_extension = thumbnail_extension.lower()

            thumbnail_filename = thumbnail_name + '_thumb' + thumbnail_extension
            thumbnail_path = os.path.join('thumbnails/', thumbnail_filename)

            # Ensure the directory exists
            thumbnail_full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_path)
            os.makedirs(os.path.dirname(thumbnail_full_path), exist_ok=True)

            if thumbnail_extension in ['.jpg', '.jpeg']:
                filetype = 'JPEG'
            elif thumbnail_extension == '.gif':
                filetype = 'GIF'
            elif thumbnail_extension == '.png':
                filetype = 'PNG'
            else:
                return

            # Save the thumbnail
            image.save(thumbnail_full_path, filetype)
            self.thumbnail = thumbnail_path
            super().save(update_fields=['thumbnail'])