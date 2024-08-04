from collections import UserDict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .util import convert_references_to_links, get_entry, list_entries, save_entry
from .forms import EntryForm, EditEntryForm, UserRegistrationForm
import random
from django.contrib import messages
from . import util
from .models import UserProfile, Entry, Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import logging
from markdown2 import markdown
import markdown2
import markdown
from django.utils.safestring import mark_safe
import re
from django.urls import reverse
from django.utils.html import format_html, escape
from .wikipedia_utils import import_wikipedia_entries


def index(request):
    entries = Entry.objects.filter(category='person', thumbnail__isnull=False).order_by('-visit_count')[:20]
    
    # Ensure there are enough entries to avoid index errors
    article_of_the_day = entries.first() if entries.exists() else None
    citizen_of_the_day = entries[15] if entries.count() > 15 else None
    on_this_day = entries[7] if entries.count() > 7 else None
    story_of_the_day = entries[19] if entries.count() > 19 else None

    return render(request, 'encyclopedia/index.html', {
        'entries': entries,
        'article_of_the_day': article_of_the_day,
        'citizen_of_the_day': citizen_of_the_day,
        'on_this_day': on_this_day,
        'story_of_the_day': story_of_the_day,
    })

def render_markdown(content):
    return markdown2.markdown(content, extras=["tables"])

def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    entries = Entry.objects.filter(tags=tag)
    return render(request, "tag_page.html", {
        "tag": tag,
        "entries": entries,
    })

def entry_page(request, title):
    entry = get_object_or_404(Entry, title=title)
    content_with_links = link_references(entry.content)
    content_with_markdown = markdown2.markdown(content_with_links, extras=["tables", "fenced-code-blocks", "strike", "highlight", "metadata"])
    content_with_markdown_safe = mark_safe(content_with_markdown)
    content_with_links = link_references(entry.content)
    bio_content_with_markdown = markdown2.markdown(entry.bio_content or "", extras=["tables", "fenced-code-blocks", "strike", "highlight", "metadata"])
    bio_content_with_markdown_safe = mark_safe(bio_content_with_markdown)
    reference = entry.reference.split(",") if entry.reference else []

    birth_date = entry.birth_date.strftime("%m-%d-%Y") if entry.birth_date else ""

    return render(request, "entry.html", {
        "entry": entry,
        "content_with_markdown_safe": content_with_markdown_safe,
        "bio_content_with_markdown_safe": bio_content_with_markdown_safe,
        "reference": reference,
        "tag": entry.tag.all(),
        "birth_date": birth_date
    })
logger = logging.getLogger(__name__)

def search(request):
    query = request.GET.get('q')

    if query:
        # Strip leading and trailing whitespace from the query
        query = query.strip()

    if not query:
        return render(request, 'encyclopedia/no_results.html', {'query': query})

    try:
        matching_entries = Entry.objects.filter(title__icontains=query)

        if matching_entries.exists():
            # If only one matching entry exists, redirect to that entry's page
            if matching_entries.count() == 1:
                return redirect('entry_page', title=matching_entries.first().title)
            # If multiple matching entries exist, render the search results page
            else:
                return render(request, 'encyclopedia/search_results.html', {
                    'query': query,
                    'search_results': matching_entries
                })
        else:
            # If no matching entries exist, render the no results page
            return render(request, 'encyclopedia/no_results.html', {
                'query': query
            })
    except Exception as e:
        # Log the error
        logger.error(f"Error during search for query '{query}': {e}")
        # Render a generic error page or redirect to a safe page
        return render(request, 'encyclopedia/no_results.html', {
            'query': query,
            'error_message': 'An error occurred during the search. Please try again.'
        })
    

@login_required
def create_new_page(request):
    if request.method == "POST":
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            form.save_m2m()
            return redirect("entry_page", title=entry.title)
    else:
        form = EntryForm()
    return render(request, "encyclopedia/create_new_page.html", {"form": form})

def link_references(content):
    # Regex patterns for different formats
    patterns = [
        re.compile(r'\[\[(.*?)\]\]'),           # [[Some Entry]]
        re.compile(r'\{\{(.*?)\}\}'),           # {{Some Entry}}
        re.compile(r'\[(.*?)\]'),               # [Some Entry]
        re.compile(r'\[(.*?)\]\((.*?)\)'),      # [Some Entry](Some Entry)
    ]

    def replace_match(match):
        entry_title = match.group(1).strip()

        try:
            entry = Entry.objects.get(title__iexact=entry_title)
            url = reverse('entry_page', args=[entry.title])
            return format_html('<a href="{}">{}</a>', url, entry_title)
        except Entry.DoesNotExist:
            return match.group(0)  # If entry doesn't exist, return original match

    for pattern in patterns:
        content = pattern.sub(replace_match, content)

    return content

def random_page(request):
    random_entry = Entry.objects.order_by('?').first()
    return redirect('entry_page', title=random_entry.title)

@login_required
def edit_page(request, title):
    entry = get_object_or_404(Entry, title=title)
    if request.method == "POST":
         form = EditEntryForm(request.POST, request.FILES, instance=entry)
         if form.is_valid():
            entry = form.save(commit=False)
            form.save_m2m()  # Save the many-to-many data for tags
            entry.save()
            return redirect('entry_page', title=entry.title)
    else:
        form = EditEntryForm(instance=entry)
    return render(request, "encyclopedia/edit_page.html", {"form": form, "title": title})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            UserProfile.objects.create(user=form.save())
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request):
    # Retrieve the UserProfile associated with the current user
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:

    # Create a new UserProfile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

def import_view(request):
    if request.method == "POST":
        import_wikipedia_entries()
        return render(request, 'import_success.html')
    return render(request, 'import.html')
