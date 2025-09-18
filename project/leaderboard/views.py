from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Profile
from .forms import SearchLeaderboard
from django.core.exceptions import ValidationError

# Create your views here.
def leaderboard(request):
    
    if request.method == "GET":

        users = User.objects.select_related("profile").order_by("-profile__points")
        return render(request, "leaderboard/results.html", {"users": users})
    
    if request.method == "POST":
        form = SearchLeaderboard(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if User.objects.filter(username=query).count() > 0:
                user = User.objects.get(username=query)
                
            else:
                raise ValidationError("Username does not exist")
            return render(request, "leaderboard/search.html", {"user": user})
                