from django.urls import path
from .views import leaderboard


urlpatterns = [
    path("leaderboard/", leaderboard, name="leaderboard_results"),
]