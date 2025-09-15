from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# homepage links 
def index (request):
    return render(request, "index.html")

def about (request):
    return render(request, "about.html")

def signup (request):
    return render(request, "signup.html")

def leaderboard (request):
    return render(request , "leaderboard.html")

def login (request):
    return render(request, "login.html")


# when the user is logged in 
def user_home (request):
    return render(request, "user/user_home.html")

def profile (request):
    return render(request, "user/profile.html")