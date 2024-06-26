from collections import UserDict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .util import get_entry, list_entries, save_entry
from .forms import EntryForm, EditEntryForm, UserRegistrationForm
import random
from django.contrib import messages
from . import util
from .models import UserProfile, Entry
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import logging
from markdown2 import markdown
from .util import link_references

def index(request):
    entries = list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    }) 

def entry_page(request, title):
    # Retrieve the entry object from the database or return a 404 error if not found
    entry = get_object_or_404(Entry, title=title)
    
    # Optionally, you can retrieve the entry content and convert it to HTML using markdown2
    # html_content = markdown2.markdown(entry.content)
    
    # Pass the entry object to the template for rendering
    return render(request, "entry.html", {"entry": entry})

logger = logging.getLogger(__name__)   

def search(request):
    query = request.GET.get('q')
    
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
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            image = form.cleaned_data.get("image")
            category = form.cleaned_data.get("category")
            tag = form.cleaned_data.get("tag")
            reference = form.cleaned_data.get("reference")
            
            if Entry.objects.filter(title__iexact=title).exists():
                messages.error(request, f"An entry with the title '{title}' already exists.")
            else:
                content_html = markdown(content)
                content_html = link_references(content_html)
                entry = Entry(title=title, content=content_html, image=image, category=category, tag=tag, reference=reference)
                entry.save()
                return redirect("entry_page", title=title)
    else:
        form = EntryForm()
    return render(request, "encyclopedia/create_new_page.html", {"form": form})

def random_page(request):
    random_entry = Entry.objects.order_by('?').first()
    return redirect('entry_page', title=random_entry.title)

@login_required
def edit_page(request, title):
    entry = get_object_or_404(Entry, title=title)
    if request.method == "POST":
        form = EditEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            content = form.cleaned_data["content"]
            entry.content = markdown(content)
            entry.content = link_references(entry.content)
            form.save()
            return redirect('entry_page', title=title)
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