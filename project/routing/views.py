from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

# homepage links 
def index (request):
    return render(request, "index.html")

def about (request):
    return render(request, "about.html")

def signup (request):
    return render(request, "signup.html")

def leaderboard (request):
    return render(request, "leaderboard/results.html")

def login (request):
    return render(request, "login.html")


# when the user is logged in 
@login_required
def user_home (request):
    return render(request, "user/user_home.html")

@login_required
def profile (request):
    return render(request, "user/profile.html")

@login_required
def search (request):
    return render(request, "books/search_books.html")

@login_required
def bookshelf (request):
    return render(request, "user/bookshelf/bookshelf.html")

@login_required
def friends (request):
    return render(request, "user/friends/friends.html")

# check challenges.urls for challenges view --> 'load_challenges_page'