from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    entry_md = util.get_entry(entry)
    if entry_md == None:
        return render(request, "encyclopedia/none.html", {
        "title": entry,
        "missing": "This entry doesn't exist :("
    })
    else:
        entry_content = markdowner.convert(entry_md)
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "entry": entry_content
        })
    
def search(request):
    if request.method == "POST":
        search_q = request.POST['q']
        markdowner = Markdown()
        entry_md = util.get_entry(search_q)
        if entry_md is not None:
            entry_content = markdowner.convert(entry_md)
            return render(request, "encyclopedia/entry.html", {
                "title": search_q,
                "entry": entry_content
            })
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if search_q.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search-results.html", {
                "results": results
            })

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        entry_exist = util.get_entry(title)
        if entry_exist is not None:
            return render(request, "encyclopedia/none.html", {
                "missing": "This entry already exist!"
            })
        else:
            util.save_entry(title, content)
            markdowner = Markdown()
            entry_md = util.get_entry(title)
            entry_content = markdowner.convert(entry_md)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": entry_content
            })
        
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        markdowner = Markdown()
        entry_md = util.get_entry(title)
        entry_content = markdowner.convert(entry_md)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_content
        })
    
def aleatorio(request):
    entries = util.list_entries()
    aleatorio = random.choice(entries)
    markdowner = Markdown()
    entry_md = util.get_entry(aleatorio)
    entry_content = markdowner.convert(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "title": aleatorio,
        "entry": entry_content
    })
