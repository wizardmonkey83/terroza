from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
        # Return an 'invalid login' error message.
        form = LoginForm()
    
    return render(request, "registration/login.html", {"form": form})


@login_required
def display_profile(request):

    if request.method == "GET":
    
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None

        user_data = []
        if user_profile:
            username = request.user.username
            total_points = request.user.profile.points
            books_read = request.user.profile.books_read
            words_written = request.user.profile.words_written
            entries_made = request.user.profile.entries_made
            global_rank = request.user.profile.global_rank
            profile_picture = request.user.profile.profile_picture
            joined_on = request.user.date_joined
            pages_read = request.user.profile.pages_read

            user_data.append({
                "username": username,
                "total_points": total_points,
                "books_read": books_read,
                "words_written": words_written,
                "entries_made": entries_made,
                "global_rank": global_rank,
                "profile_picture": profile_picture,
                "joined_on": joined_on,
                "pages_read": pages_read
            })

            return render(request, "user/profile.html", {"user": user_data})
        
    
