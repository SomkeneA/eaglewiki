from django.conf import settings
from django.db import models
from django.urls import reverse
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
        # Save the entry to generate the image file path if it doesn't exist
        super().save(*args, **kwargs)
        if self.image:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        if not self.image:
            return

        image = Image.open(self.image.path)
        image.thumbnail((200, 200), Image.LANCZOS)

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
        # Save the entry again to update the thumbnail path
        super().save(update_fields=['thumbnail'])

    def get_absolute_url(self):
        return reverse('entry_page', args=[str(self.title)])