from django.urls import path
from .views import load_send_challenge_request, send_challenge_request, load_challenge_page, load_past_challenges, load_challenge_overview, accept_challenge_request, remove_challenge_request, load_pending_challenge_requests

urlpatterns = [
    path("challenges/", load_challenge_page, name="load_challenge_page"),
    path("challenges/load_send/", load_send_challenge_request, name="load_send_challenge_request"),
    path("challenges/send/", send_challenge_request, name="send_challenge_request"),
    path("challenges/past/", load_past_challenges, name="load_past_challenges"),
    path("challenges/pending/", load_pending_challenge_requests, name="load_pending_challenge_requests"),
    path("challenges/overview/", load_challenge_overview, name="load_challenge_overview"),
    path("challenges/accept/", accept_challenge_request, name="accept_challenge_request"),
    path("challenges/remove/", remove_challenge_request, name="remove_challenge_request"),
]