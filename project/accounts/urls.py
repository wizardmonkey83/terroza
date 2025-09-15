from django.urls import path
from .views import display_profile, signup_view, login_view


urlpatterns = [
    # automatically calls 'signup_view' when the signup page is visited
    path("signup/", signup_view, name="signup"),
    path("profile/", display_profile, name="diplay_profile"),
    path("login/", login_view, name="login")
]