from django.conf import settings
from django.db import models
from django.urls import reverse
from PIL import Image, UnidentifiedImageError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
import logging
import os

logging.basicConfig(
    filename='thumbnail_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
) 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Add other fields as needed

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Entry(models.Model):

    CATEGORY_CHOICES = [
        ('people & organization', 'People & Organization'),
        ('person', 'Person'),
        ('event', 'Event'),
        ('entertainment', 'Entertainment'),
        ('place & geography', 'Place & Geography'),
        ('technology & innovation', 'Technology & Innovation'),
        ('religion & culture', 'Religion & Culture'),
        ('food & agriculture', 'Food & Agriculture'),
        ('name', 'Name'),
        ('language', 'Language'),
        ('education', 'Education'),
        ('book', 'Book')
    ]

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    tag = models.ManyToManyField(Tag, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    bio_content = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    visit_count = models.IntegerField(default=0)

    def entry_detail(request, pk):
        entry = get_object_or_404(Entry, pk=pk)
        entry.visit_count += 1
        entry.save()
        return render(request, 'encyclopedia/entry_detail.html', {'entry': entry})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            try:
                self.generate_thumbnail()
            except UnidentifiedImageError as e:
                logging.error(f"Failed to generate thumbnail for {self.image.path}: {e}")

    def generate_thumbnail(self):
        try:
            with Image.open(self.image.path) as image:
                image.thumbnail((300, 300))
                thumbnail_path = self.get_thumbnail_path()
                image.save(thumbnail_path)
                # Store the path relative to the media root
                relative_thumbnail_path = os.path.relpath(thumbnail_path, 'media')
                self.thumbnail = relative_thumbnail_path
                super().save(update_fields=['thumbnail'])
        except UnidentifiedImageError as e:
            logging.error(f"Failed to open image file {self.image.path}: {e}")
        except Exception as e:
            logging.error(f"An error occurred while generating thumbnail for {self.image.path}: {e}")

    def get_thumbnail_path(self):
        filename, ext = os.path.splitext(os.path.basename(self.image.path))
        thumbnail_dir = os.path.join(os.path.dirname(self.image.path), 'thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)
        return os.path.join(thumbnail_dir, f'{filename}_thumb{ext}')

    def get_absolute_url(self):
        return reverse('entry_page', args=[str(self.title)])
