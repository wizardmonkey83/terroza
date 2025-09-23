from django.shortcuts import render, redirect
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
    if request.user.is_authenticated:
        return render(request, "user/user_home.html")

def profile (request):
    if request.user.is_authenticated:
        return render(request, "user/profile.html")

def search (request):
    if request.user.is_authenticated:
        return render(request, "books/search_books.html")
    
def bookshelf (request):
    if request.user.is_authenticated:
        return render(request, "user/bookshelf/bookshelf.html")