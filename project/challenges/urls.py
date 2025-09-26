from django.urls import path
from .views import load_send_challenge_request, load_challenge_page, load_past_challenges, load_challenge_overview, accept_challenge_request, remove_challenge_request

urlpatterns = [
    path("challenges/", load_challenge_page, name="load_challenge_page"),
    path("challenges/send/", load_send_challenge_request, name="load_send_challenge_request"),
    path("challenges/past/", load_past_challenges, name="load_past_challenges"),
    path("challenges/overview/", load_challenge_overview, name="load_challenge_overview"),
    path("challenges/accept/", accept_challenge_request, name="accept_challenge_request"),
    path("challenges/remove/", remove_challenge_request, name="remove_challenge_request"),
]