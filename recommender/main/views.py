from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User 



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
        return redirect('/sim')
    else: 
        return redirect('/login?error=True')

def signup(request):
    user = User.objects.create_user(
        username = request.POST['username'],
        password = request.POST['password'],
        email = request.POST['email']
    )
    login(request, user)
    return redirect('/home')
