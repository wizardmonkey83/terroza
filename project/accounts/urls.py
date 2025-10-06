from django.urls import path
from .views import signup_view, login_view, send_friend_request, accept_friend_request, remove_friend, remove_friend_request, load_send_friend_request, load_pending_requests, load_remove_friend_caution, load_delete_account_caution, delete_account, logout_view


urlpatterns = [
    # signup/login/delete
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("delete_caution/", load_delete_account_caution, name="load_delete_account_caution"),
    path("delete/", delete_account, name="delete_account"),
    path("logout/", logout_view, name="logout_view"),

    # friends
    path("friends/add/", send_friend_request, name="send_friend_request"),
    path("friends/remove_caution/", load_remove_friend_caution, name="load_remove_friend_caution"),
    path("friends/accept/", accept_friend_request, name="accept_friend_request"),
    path("friends/remove/", remove_friend, name="remove_friend"),
    path("friends/remove_request/", remove_friend_request, name="remove_friend_request"),
    path("friends/load_request/", load_send_friend_request, name="load_send_friend_request"),
    path("friends/notifications/", load_pending_requests, name="load_pending_requests"),
]