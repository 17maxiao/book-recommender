from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from main.models import ShelfEntry
import markdown2
from markdown2 import Markdown




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
    if request.method == "POST":
        entry = ShelfEntry(
            title = request.POST["title"],
            body = markdown2.markdown(request.POST["body"]),
            topic = request.POST["topic"]
        )
        entry.save()
        
    entries = ShelfEntry.objects.all()
    return render(request, 'shelf.html', {'entries': entries})
