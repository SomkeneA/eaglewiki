from django.shortcuts import render, redirect
from django.http import Http404
from .util import get_entry, list_entries, save_entry
from .forms import EntryForm
import random
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

def search(request):
    query = request.GET.get('q')
    entries = list_entries()

    # Check if the query matches the name of an encyclopedia entry
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if matching_entries:
        # If there are matching entries, redirect to the first matching entry page
        return redirect('entry_page', title=matching_entries[0])
    else:
        # If there are no matching entries, display search results page
        search_results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, 'search_results.html', {'query': query, 'search_results': search_results})

def create_new_page(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            save_entry(title, content)  # Save the new entry
            return redirect("entry_page", title=title)  # Redirect to the newly created entry page
    else:
        form = EntryForm()

    return render(request, "create_new_page.html", {"form": form})

def random_page(request):
    entries = list_entries()
    random_entry = random.choice(entries)
    return redirect('entry_page', title=random_entry)