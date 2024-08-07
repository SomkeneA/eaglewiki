import re
from django.urls import reverse
from .models import Entry
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    """
    Returns a list of all titles of encyclopedia entries stored in the database.
    """
    return Entry.objects.all()


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and content. If an existing
    entry with the same title already exists, it is replaced.
    """
    entry, _ = Entry.objects.update_or_create(title=title, defaults={'content': content})
    return entry

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        entry = Entry.objects.get(title=title)
        return entry.content
    except Entry.DoesNotExist:
        return None
    
def convert_references_to_links(content):
    def replace_reference(match):
        title = match.group(1)
        return f'[{title}](/wiki/{title})'
    return re.sub(r'\[\[([^\]]+)\]\]', replace_reference, content)