from django.urls import path
from .views import SignUpView


urlpatterns = [
    path("books/", SignUpView.as_view(), name="books"),
]