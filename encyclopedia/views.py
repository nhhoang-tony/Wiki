from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

import random
from . import util

import markdown2

# return homepage
def index(request):
    entries = util.list_entries()
    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "encyclopedia/index.html", {
        "entries": page_obj
    })


# generate each wiki page by retrieving from folder entries
def generate_page(request, title):
    # get page content from entries folder
    page = util.get_entry(title)

    # if page doesn't exist
    if (page == None):
        return render(request, "encyclopedia/page.html", {
            "title": title, # return page title
            "content": "Apology, page does not exist", # return apology message
            "message": "none"
        })

    # if page exist, render page to user
    else:
        return render(request, "encyclopedia/page.html", {
            "title": title, # return page title
            "content": markdown2.markdown(page) # return wiki content
        })

# search request when user type in post title
def search_page(request):
    # only allow users to reach this page via POST method as by using search bar
    if request.method == "POST":
        # search for post with user's query as title
        title = request.POST["q"]

        if ("*" in title or "?" in title or "\"" in title or
            ":" in title or "/" in title or "<" in title or
            ">" in title or "\\" in title or "|" in title):
            return render(request, "encyclopedia/search.html", {   
                "keyword": title
            })

        page = util.get_entry(title)

        # if page doesn't exist, return user to all page titles that contains user's query
        if (page == None):
            # list of all page titles that contain user's query
            entries = []

            # first get all page titles
            all_entries = util.list_entries()

            # get only pages that contain user's query
            for all_entry in all_entries:
                if (title.upper() in all_entry.upper()): # allow for case insensitive search
                    entries.append(all_entry)
        
            return render(request, "encyclopedia/search.html", {
                "entries": entries, # return apology message
                "keyword": title
            })

        # if page exist, render page to user
        else:
            return HttpResponseRedirect(reverse('page', args=(title, )))

# allow users upload new wiki page
def new_page(request):
    # if users reach route via GET request
    if request.method == "GET":
        # return POST form for users to enter page
        return render(request, "encyclopedia/new_page.html", {
            "title": "Post new page"
        })

    # if users reach route via POST as by submitting form
    elif request.method == "POST":
        # get page details from users
        title = request.POST["title_page"]
        body = request.POST["body_page"].encode('utf8')

        # check if new page is empty
        if (title == "" or body.decode('utf8') == ""):
            return render(request, "encyclopedia/new_page.html", {
                "message": "Title or page content must not be empty. Please try again",
                "page_title": title,
                "page_body": body.decode('utf8')
            })

        # check for existing page in database
        if (util.get_entry(title) != None):
            # return error message to users
            return render(request, "encyclopedia/new_page.html", {
                "message": "There is already a page with the same name, please try again",
                "page_title": title,
                "page_body": body
            })

        # if no existing page, enter new page into database
        util.save_entry(title, '#{}\r\n'.format(title).encode('utf8') + body)

        # return user to newly added page
        return HttpResponseRedirect(reverse('page', args=(title, )))

# allow users to edit current wiki page
def edit_page(request, title):
    # if users reach route via GET request
    if request.method == "GET":
        # get current post content from database
        page = util.get_entry(title)

        # return POST form for users to edit page
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": page
        })
        
    # if users reach route via POST as by submitting form
    elif request.method == "POST":
        # get new page details from user
        body = request.POST["body_page"].encode('utf8')

        # check if new page is empty
        if (body.decode('utf8') == ""):
            page = util.get_entry(title)

            return render(request, "encyclopedia/edit_page.html", {
                "message": "Page content cannot be empty",
                "title": title,
                "content": page
        })

        # update existing page
        util.save_entry(title, body)

        # return user to newly editted page
        return HttpResponseRedirect(reverse('page', args=(title, )))

# generate a random wiki page by retrieving from folder entries
def random_page(request):
    # render random page to users
    return HttpResponseRedirect(reverse('page', args=(random.choice(util.list_entries()), )))


