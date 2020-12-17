from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from main.models import ShelfEntry
import markdown2
from markdown2 import Markdown
import csv
from pathlib import Path
from main.helpers import getresults





# Create your views here.

def home(request):
    return render(request, "home.html", {})

def login_view(request):
    return render(request, "login.html", {})

def signin(request): 
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/shelf')
    else: 
        return redirect('/login?error=True')

def signup(request):
    user = User.objects.create_user(
        username = request.POST['username'],
        password = request.POST['password'],
        email = request.POST['email']
    )
    login(request, user)
    return redirect('/shelf')



def shelf(request): 

    if not request.user.is_authenticated:
        return redirect('/login_view')


    entries = ShelfEntry.objects.filter(author=request.user)
    # matchedbooks = []
    # if request.method == "POST":
    #     title = request.POST["title"]
    #     reader = csv.reader(open('df_books.csv'))
    #     for row in reader:
    #         if title in row[title]:
    #             matchedbooks.append(row[title])
    return render(request, 'shelf.html', {'entries': entries})


def search(request):
    if request.method == "GET":
        searched = request.GET["title"]
        searched = str(searched)
        print("hello")
        print(type(searched))
        matchedbooks = getresults(searched)
    return render(request, 'results.html',{'searched': searched, 'matchedbooks': matchedbooks})

def results(request):
    pass
    # if request.method == "POST":
    #     entry = ShelfEntry(
    #         title = title,
    #         body = request.POST["body"],
    #         rating = request.POST["rating"]
    #     )
    #     entry.save()
    
    # return render(request,'results.html', {'title': title},{'entries': entries})

def addtoshelf(request, title):
    
    if request.method == "POST":
        entry = ShelfEntry.objects.create(
            title = title,
            review = request.POST["review"],
            rating = request.POST["rating"],
            author = request.user
        )
        #entry.save()
        return redirect('/shelf')
    #print(entry.title)
    return render(request,'addtoshelf.html', {'title': title})


def entry(request, id):
    entry = ShelfEntry.objects.get(id=id)
    return render(request, "entry.html", {'entry': entry}) 