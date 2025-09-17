from django.urls import path
from .views import search_books, add_book


urlpatterns = [
    path("books/", search_books, name="search_books"),
    # in the future dont put two view functions on same file path or you'll spend 8 hours smashing your head against a wall
    path("books/add/", add_book, name="add_book"),
]