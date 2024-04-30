from collections import UserDict
from django.shortcuts import render, redirect
from django.http import Http404
from .util import get_entry, list_entries, save_entry
from .forms import EntryForm, EditEntryForm, UserRegistrationForm
import random
from django.contrib import messages
from . import util
import markdown2
from .models import UserProfile, Entry
from django.contrib.auth.models import User

def index(request):
    entries = Entry.objects.all()  # Fetch all entries from the database
    return render(request, 'index.html', {'entries': entries})

def entry_page(request, title):
    # Retrieve the contents of the entry with the provided title
    entry_content = get_entry(title)

    # Check if the entry exists

    if entry_content is None:
        return render(request, "not_found.html", {"title": title})
    html_content = markdown2.markdown(entry_content)
    return render(request, "entry.html", {"title": title, "entry_content": html_content})
    # Render the entry page template with the entry content

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
            existing_entries = list_entries()
            if title.lower() in [entry.lower() for entry in existing_entries]:
                messages.error(request, f"An entry with the title '{title}' already exists.")
            else:
                save_entry(title, content)  # Save the new entry
            return redirect("entry_page", title=title)  # Redirect to the newly created entry page
    else:
        form = EntryForm()

    return render(request, "create_new_page.html", {"form": form})

def random_page(request):
    entries = list_entries()
    random_entry = random.choice(entries)
    return redirect('entry_page', title=random_entry)

def edit_page(request, title):
    content = get_entry(title)
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            save_entry(title, new_content)
            return redirect('entry_page', title=title)
    else:
        form = EditEntryForm(initial={"content": content})
    return render(request, "edit_page.html", {"form": form, "title": title})

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
    custom_user = User.objects.get(id=request.user.id)
    user_profile = UserProfile.objects.get(user=custom_user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)