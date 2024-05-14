from collections import UserDict
from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry_page(request, title):
    # Retrieve the entry object from the database or return a 404 error if not found
    entry = get_object_or_404(Entry, title=title)
    
    # Optionally, you can retrieve the entry content and convert it to HTML using markdown2
    # html_content = markdown2.markdown(entry.content)
    
    # Pass the entry object to the template for rendering
    return render(request, "entry.html", {"entry": entry})

def search(request):
    query = request.GET.get('q')
    matching_entries = Entry.objects.filter(title__icontains=query)

    if matching_entries.exists():
        return redirect('entry_page', title=matching_entries.first().title)
    else:
        return render(request, 'search_results.html', {'query': query, 'search_results': matching_entries})

def create_new_page(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if Entry.objects.filter(title__iexact=title).exists():
                messages.error(request, f"An entry with the title '{title}' already exists.")
            else:
                save_entry(title, content)  # Save the new entry
                return redirect("entry_page", title=title)  # Redirect to the newly created entry page
    else:
        form = EntryForm()

    return render(request, "create_new_page.html", {"form": form})

def random_page(request):
    random_entry = Entry.objects.order_by('?').first()
    return redirect('entry_page', title=random_entry.title)

def edit_page(request, title):
    entry = Entry.objects.get(title=title)
    if request.method == "POST":
        form = EditEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_page', title=title)
    else:
        form = EditEntryForm(instance=entry)
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