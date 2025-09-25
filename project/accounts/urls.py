from django.urls import path
from .views import signup_view, login_view, send_friend_request, accept_friend_request, remove_friend, remove_friend_request, friends_list, load_send_friend_request, load_pending_requests


urlpatterns = [
    # automatically calls 'signup_view' when the signup page is visited
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("friends/", friends_list, name="friends_list"),
    path("friends/add/", send_friend_request, name="send_friend_request"),
    path("friends/accept/", accept_friend_request, name="accept_friend_request"),
    path("friends/remove/", remove_friend, name="remove_friend"),
    path("friends/remove_request/", remove_friend_request, name="remove_friend_request"),
    path("friends/load_request/", load_send_friend_request, name="load_send_friend_request"),
    path("friends/notifications/", load_pending_requests, name="load_pending_requests"),
]