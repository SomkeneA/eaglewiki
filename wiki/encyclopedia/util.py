import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """

    try:
        with default_storage.open(f"entries/{title}.md", 'rb') as f:
            content = f.read()
            # Try decoding the content using UTF-8
            try:
                decoded_content = content.decode("utf-8")
                return decoded_content
            except UnicodeDecodeError:
                # If decoding fails, try a different encoding or handle the error as needed
                return None
    except FileNotFoundError:
        return None
