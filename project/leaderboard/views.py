from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def leaderboard(request):
    if request.method == "GET":
        user = request.user
        friends = user.profile.friends.order_by("-profile__points")
        return render(request, "leaderboard/results.html", {"friends": friends})
                