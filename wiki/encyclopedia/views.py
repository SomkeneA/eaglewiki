from django.shortcuts import render, Http404
from .util import get_entry

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    # Retrieve the contents of the entry with the provided title
    entry_content = get_entry(title)

    # Check if the entry exists
    if entry_content is None:
        # Raise a 404 Not Found exception if the entry does not exist
        raise Http404("Entry does not exist")

    # Render the entry page template with the entry content
    return render(request, "entry.html", {
        "title": title,
        "content": entry_content
    })