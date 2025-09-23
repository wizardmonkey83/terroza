from django.urls import path
from .views import search_books, add_book, load_entry, save_entry


urlpatterns = [
    path("books/", search_books, name="search_books"),
    # in the future dont put two view functions on same file path or you'll spend 2 hours smashing your head against a wall
    path("books/add/", add_book, name="add_book"),
    path("bookshelf/entry/", load_entry, name="load_entry"),
    path("bookshelf/save/", save_entry, name="save_entry"),
]