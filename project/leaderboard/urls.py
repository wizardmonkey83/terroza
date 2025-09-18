from django.urls import path
from .views import leaderboard


urlpatterns = [
    path("leaderboard/", leaderboard, name="leaderboard_results"),
    path("leaderboard/search/", leaderboard, name="search_leaderboard"),
]