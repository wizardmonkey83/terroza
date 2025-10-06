from django.urls import path
from .views import search_books, add_book, load_entry, save_entry, load_add_books, load_remove_book_caution, remove_book, load_view_entries, load_past_books, book_overview


urlpatterns = [
    path("books/", search_books, name="search_books"),
    # in the future dont put two view functions on same file path or you'll spend 2 hours smashing your head against a wall
    path("books/add/", add_book, name="add_book"),
    path("books/load_add/", load_add_books, name="load_add_books"),
    path("bookshelf/entry/", load_entry, name="load_entry"),
    path("bookshelf/save/", save_entry, name="save_entry"),
    path("bookshelf/remove_caution/", load_remove_book_caution, name="load_remove_book_caution"),
    path("bookshelf/remove/", remove_book, name="remove_book"),
    path("bookshelf/view_entries/", load_view_entries, name="load_view_entries"),
    path("bookshelf/past/", load_past_books, name="load_past_books"),
    path("bookshelf/overview/", book_overview, name="book_overview"),

]