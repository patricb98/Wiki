from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django import forms

import random
from . import util

# VIEW PAGE TITLE OR SEARCH RESULTS
def index(request):
    # navbar search query request
    if request.method == "GET" and "q" in request.GET:
        # normalise search request 
        query = request.GET.get("q","").strip().lower() 
        # get all wiki entries 
        all_entries = util.list_entries()
        # filter matching entries 
        matching_entries = [entry for entry in all_entries if query in entry.lower()]

        # redirect exact match
        if len(matching_entries) == 1 and query == matching_entries[0].lower():
            return redirect("title", title=matching_entries[0])
        
        # render search results page if no match
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": matching_entries
        })

    # default render index page with all entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# VIEW PAGE TITLE
def title(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
            "message": f"The page '{title}' does not exist."
        }))
    return render(request, "encyclopedia/title.html", {
        "entry": util.get_entry(title),
        "title": title
    })

# NEW PAGE
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def new_page(request):
    #check method is POST
    if request.method == "POST":

        # take in the data from user submission
        form = NewPageForm(request.POST)

        # check form is valid (server side)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"]

            # check if page exists
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error_message": f"A page with the title: '{title}' already exists"
                })
            
            # save new page to app
            util.save_entry(title, content)

            # redirect the user to the new saved page
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "entry": content
            })

    # if GET request create a blank form 
    else:
        form = NewPageForm()
    
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

# EDIT PAGE
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def edit_page(request, title):
    # GET the entry content
    entry = util.get_entry(title)
    if entry is None:
        return HttpResponseNotFound(render(request, "encyclopedia/error.html", {
            "message": f"The page '{title}' does not exist."
        }))
    
    # check method is POST
    if request.method == "POST":

        # take in data from user submission
        form = EditPageForm(request.POST)

        # check form is valid
        if form.is_valid():
            content = form.cleaned_data["content"]

            # save content and title
            util.save_entry(title, content)

            # render user to new saved page
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "entry": content
            })
    
    # if GET request prefill form with current content
    else:
        form = EditPageForm(initial={"content": entry})
    
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

# RANDOM PAGE
def random_page(request):
    # get all entries
    all_entries = util.list_entries()

    # select a random entry
    if all_entries:
        random_entry = random.choice(all_entries)

        #redirect to random entry
        return redirect("title", title=random_entry)

    # if no entries exist show error
    return render(request, "encyclopedia/error.html", {
        "message": "No entries available for random page"
    })