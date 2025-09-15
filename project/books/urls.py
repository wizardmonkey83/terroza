from django.urls import path
from .views import search_books, add_book


urlpatterns = [
    path("books/", search_books, name="search_books"),
    path("books/", add_book, name="add_book"),
]