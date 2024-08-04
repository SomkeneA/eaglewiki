from django.core.management.base import BaseCommand
from encyclopedia.models import Entry
from PIL import Image, UnidentifiedImageError
import logging
import os

logging.basicConfig(
    filename='generate_thumbnails.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Generate thumbnails for entries with existing images but no thumbnails'

    def handle(self, *args, **kwargs):
        entries = Entry.objects.filter(image__isnull=False, thumbnail__isnull=True)
        for entry in entries:
            try:
                if entry.image and os.path.exists(entry.image.path):
                    self.generate_thumbnail(entry)
                else:
                    self.stdout.write(self.style.WARNING(f"No file associated with image field for {entry.title}"))
            except UnidentifiedImageError as e:
                logging.error(f"Failed to generate thumbnail for {entry.image.path}: {e}")
            except Exception as e:
                logging.error(f"An error occurred while generating thumbnail for {entry.image.path}: {e}")

    def generate_thumbnail(self, entry):
        try:
            with Image.open(entry.image.path) as image:
                image.thumbnail((300, 300))
                thumbnail_path = self.get_thumbnail_path(entry)
                image.save(thumbnail_path)
                # Store the path relative to the media root
                relative_thumbnail_path = os.path.relpath(thumbnail_path, 'media')
                entry.thumbnail = relative_thumbnail_path
                entry.save(update_fields=['thumbnail'])
                self.stdout.write(self.style.SUCCESS(f"Generated thumbnail for {entry.title}"))
        except UnidentifiedImageError as e:
            logging.error(f"Failed to open image file {entry.image.path}: {e}")
        except Exception as e:
            logging.error(f"An error occurred while generating thumbnail for {entry.image.path}: {e}")

    def get_thumbnail_path(self, entry):
        filename, ext = os.path.splitext(os.path.basename(entry.image.path))
        thumbnail_dir = os.path.join(os.path.dirname(entry.image.path), 'thumbnails')
        os.makedirs(thumbnail_dir, exist_ok=True)
        return os.path.join(thumbnail_dir, f'{filename}_thumb{ext}')
