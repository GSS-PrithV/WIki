from django.shortcuts import render

import http
from http.client import HTTPResponse
from django.http import HttpResponseRedirect
import random
from . import util
from django import forms 
import re 
import markdown2
from markdown2 import Markdown 

md = Markdown()


class input(forms.Form):
    query = forms.CharField(label="Search")

class creates(forms.Form):
    newtitle = forms.CharField(label="NewTitle")
    newInfo = forms.CharField(label="Info", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))

def index(request):
    form = input()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "temp": form
    })

def wiki(request, title):
    form = input()
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", { "entry": "The page you have requested is not avaiable."})
    else:
       return render(request, "encyclopedia/entrypage.html", {
        "title": title,
        "entry": md.convert(util.get_entry(title)),
        "temp": form
    })

def search(request):
    if request.method == "POST":
        temp = input(request.POST)
        if temp.is_valid():
            it = temp.cleaned_data.get("query")
            for entry in util.list_entries():
                if it == entry:
                    return render(request, "encyclopedia/entrypage.html", {
                        "title": it,
                        "entry":  md.convert(util.get_entry(entry)),
                        "temp": temp
                    })
            substrings = []
            for entry in util.list_entries():
                if it in entry:
                    substrings.append(entry)
            if len(substrings) == 0:
                 return render(request, "encyclopedia/error.html", { 
                "entry":  "Please enter a valid query",
                "temp": temp
                }) 
            else:
                 return render(request, "encyclopedia/index.html", {
                "entries": substrings, 
                 "temp": temp
                 })
        
def create(request):
    form = input()
    if request.method == "POST":
        temp = creates(request.POST)
        if temp.is_valid():
            t = temp.cleaned_data.get("newtitle")
            content = temp.cleaned_data.get("newInfo")
            for entry in util.list_entries():
                if t == entry:
                    return render(request, "encyclopedia/error.html", { 
                    "entry":  "This page is already in the encyclopedia",
                    "temp": form
                    }) 
            util.save_entry(t,content)
            return render(request, "encyclopedia/entrypage.html",{
                "entry": md.convert(util.get_entry(t)),
                "temp": form,
                "title": t
            })
    else:
        createform = creates()
        return render(request, "encyclopedia/create.html", {
        "temp": form, 
        "createtemp": createform
        })

def edit(request,title):
    form = input()
    if request.method == "POST":
        temp = creates(request.POST)
        if temp.is_valid():
            t = temp.cleaned_data.get("newtitle")
            content = temp.cleaned_data.get("newInfo")
            util.save_entry(t,content)
            return render(request, "encyclopedia/entrypage.html",{
                "entry": md.convert(util.get_entry(t)),
                "temp": form,
                "title": title
            })
    else:
        editform = creates({
            "newtitle": title,
            "newInfo": util.get_entry(title)
        })
        return render(request, "encyclopedia/edit.html", {
        "toe": title,
        "temp": form, 
        "edit": editform
        })

def randomm(request):
    form = input()
    i = random.randint(0,len(util.list_entries())-1)
    x = 0
    for entry in util.list_entries():
        if x == i:
            return render(request, "encyclopedia/entrypage.html",{
                "entry": md.convert(util.get_entry(entry)),
                "temp": form,
                "title": entry
            })
        x = x + 1
    