import os
from django.core.management.base import BaseCommand
from encyclopedia.models import Entry


class Command(BaseCommand):
    help = 'Import existing entries into the database'

    def handle(self, *args, **options):
        entries_dir = "entries"  # Update this with the path to your entries directory

        for filename in os.listdir(entries_dir):
            if filename.endswith(".md"):
                with open(os.path.join(entries_dir, filename), "r") as file:
                    title = os.path.splitext(filename)[0]  # Extract title from filename
                    content = file.read()

                Entry.objects.create(title=title, content=content)
                self.stdout.write(self.style.SUCCESS(f"Entry '{title}' imported successfully."))