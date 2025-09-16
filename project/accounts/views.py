from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login


def signup_view(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # creates instance of User class and creates an individual user
            user = form.save()
            # creates profile model alongside the user
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("user_home")
        
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_home")
            
    else:
        form = LoginForm()
    
    return render(request, "registration/login.html", {"form": form})
        
    
