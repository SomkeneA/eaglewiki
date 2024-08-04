import wikipediaapi
from django.core.management.base import BaseCommand
from encyclopedia.models import Entry

class Command(BaseCommand):
    help = 'Import Nigerian Wikipedia entries'

    def handle(self, *args, **options):
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        )

        entries = [
   'Jukunoid languages'] # Add more entries as needed

        for entry_name in entries:
            page = wiki_wiki.page(entry_name)
            if page.exists():
                print(f"Importing: {page.title}, Content length: {len(page.text)}, URL: {page.fullurl}")
                self.save_entry_to_database(page.title, page.text)

    def save_entry_to_database(self, title, content):
        entry, created = Entry.objects.update_or_create(
            title=title,
            defaults={'content': content}
        )
        entry.save()
