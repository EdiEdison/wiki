from django.shortcuts import render, Http404, redirect
import random

from . import util
import markdown


from django.shortcuts import render, redirect
from . import util


def index(request):
    if request.method == "POST":
        search_query = request.POST.get("q", "").strip()
        if search_query:
            entry = util.get_entry(search_query)
            if entry:
                return redirect("entry", title=search_query)

            partial_matches = [
                entry for entry in util.list_entries() if search_query in entry
            ]
            return render(
                request,
                "encyclopedia/search_results.html",
                {"search_query": search_query, "results": partial_matches},
            )
    else:
        return render(
            request, "encyclopedia/index.html", {"entries": util.list_entries()}
        )


def entry_page(request, title):
    markdown_content = util.get_entry(title)

    if markdown_content is None:
        return render(request, "encyclopedia/entry_not_found.html")

    html_content = markdown.markdown(markdown_content)
    context = {"entry": {"title": title, "content": html_content}}
    return render(request, "encyclopedia/entry_page.html", context)


def create_entry(request):
    if request.method == "POST":
        entry_name = request.POST["title"]
        entry_content = request.POST["content"]
        if util.get_entry(entry_name):
            print("Error!!,  entry already exists")
        else:
            util.save_entry(title=entry_name, content=entry_content)
            return redirect("entry", title=entry_name)
    return render(request, "encyclopedia/entry_create.html")


def edit_page(request, title):
    current_content = util.get_entry(title)
    context = {"title": title, "content": current_content}

    if request.method == "POST":
        updated_content = request.POST.get("content")
        util.save_entry(title, updated_content)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/edit_page.html", context)


def random_entry_page(request):
    all_entries = util.list_entries()
    if all_entries:
        random_entry = random.choice(all_entries)

        return redirect("entry", title=random_entry)
    else:
        return redirect("index")
