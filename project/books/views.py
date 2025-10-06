import requests
import os
import datetime
from decouple import config

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.
from .forms import BookEntry, BookQuery, AddBook, LoadBookEntry, ViewPastEntries, RemoveBook
from .models import ReadingLog, Book, UserBook
from challenges.models import Challenge


# SEARCHING/ADDING BOOKS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def search_books(request):

    if request.method == "POST":
        form = BookQuery(request.POST)
        if form.is_valid():
            
            # gets the user"s query from the frontend and formats it so its ready to be ingested by google books 
            user_query = form.cleaned_data["user_query"]
            formatted_user_query = user_query.replace(" ", "+")

            # performs the api search and returns a json reponse with the fields --> authors, page count, title, published date, and front cover
            api_key = config("GOOGLE_BOOKS_API_KEY")
            google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q={formatted_user_query}&fields=items(volumeInfo(authors,pageCount,title,publishedDate,imageLinks/thumbnail))&key={api_key}"
            
            try:
                response = requests.get(google_books_api_url)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as error:
                messages.error(request, f"Error message: {error}")
                return render(request, "user/friends/requests/request_response.html")
            
            books_data = []
            if "items" in data:
                for item in data["items"]:
                    # using empty dictionary to avoid triggering a KeyError if there isnt volume information availible
                    volume_info = item.get("volumeInfo", {})
                    # so that the site doesn't tweak
                    if not all(k in volume_info for k in ["pageCount", "title", "authors", "imageLinks"]):
                        continue

                    title = volume_info.get("title", "No Title Available")
                    authors = ", ".join(volume_info.get("authors", ["Unknown Author"]))
                    pages = volume_info.get("pageCount", "Page Count Unknown")
                    image_url = volume_info.get("imageLinks", {}).get("thumbnail", "")
                    point_potential = int(pages * 10) 

                    books_data.append({
                        "title": title,
                        "author": authors,
                        "pages": pages,
                        "image_url": image_url,
                        "point_potential": point_potential
                    })
            # if the user searches for a book, the above logic gets executed and HTMX reloads the html fragment containing each relevant book
            return render(request, "books/book_search_results.html", {"books": books_data})
    
    return render(request, "books/search_books.html")

@login_required
def load_add_books(request):
    if request.method == "GET":
        return render(request, "books/search_books.html")


@login_required
def add_book(request):
    if request.user.is_authenticated:
        # if the user presses "add" the books information gets stored to the database and is linked to the user
        if request.method == "POST":
            form = AddBook(request.POST)
            if form.is_valid():
                # takes the data from the HTML page and attributes it to the title within the form AddBook
                user = request.user
                title = form.cleaned_data["title"]
                author = form.cleaned_data["author"]
                page_count = form.cleaned_data["page_count"]
                point_potential = form.cleaned_data["point_potential"]
                thumbnail = form.cleaned_data["thumbnail"]

                new_book, created = Book.objects.get_or_create(title=title, author=author, cover_image=thumbnail, page_count=page_count, point_potential=point_potential)

                if not UserBook.objects.filter(user=user, book=new_book).exists():
                    UserBook.objects.create(user=user, book=new_book, reading_status="to-read")
                    messages.success(request, f"{title} was added to your bookshelf!")
                    return render(request, "user/friends/requests/request_response.html")
                else:
                    messages.error(request, f"{title} is already on your bookshelf")
                    return render(request, "user/friends/requests/request_response.html")
            
    return render(request, "books/search_books.html")

@login_required
def load_remove_book_caution(request):
    if request.method == "POST":
        form = RemoveBook(request.POST)
        if form.is_valid():
            
            user_book_id = form.cleaned_data["user_book_id"]
            user = request.user

            try:
                user_book = user.books.get(id=user_book_id)
                return render(request, "user/bookshelf/remove_book_caution.html", {"user_book": user_book})
            except:
                messages.error(request, "Unable to Remove Book")
                return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/bookshelf/bookshelf.html")

@login_required
def remove_book(request):
    if request.method == "POST":
        form = RemoveBook(request.POST)
        if form.is_valid():
            
            user_book_id = form.cleaned_data["user_book_id"]
            user = request.user

            try:
                user_book = user.books.get(id=user_book_id)
                # check if this should be .remove()
                user_book.delete()

                messages.success(request, f"{user_book.book.title} was removed from your bookshelf")
                return render(request, "user/friends/requests/request_response.html")
            except:
                messages.error(request, "Unable to Remove Book")
                return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/bookshelf/bookshelf.html")




# ENTRY STUFF -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def load_entry(request):
    # if this is a POST request to the backend
    if request.method == "POST":
        # create an instance of the form BookEntry and populate it with the data from the request (the users entry)
        form = LoadBookEntry(request.POST)
        # check to see if the user made an entry
        if form.is_valid():

            user = request.user
            user_book_id = form.cleaned_data["user_book_id"] 
            try:
                user_book = UserBook.objects.get(user=user, id=user_book_id)
                
                return render(request, "user/bookshelf/entry_card.html", {"user_book": user_book})
            except:
                messages.error(request, "Problem loading entry")
                return render(request, "user/friends/requests/request_response.html")

    return render(request, "user/bookshelf/bookshelf.html")


@login_required
def save_entry(request):

    if request.method == "POST":
        form = BookEntry(request.POST)
        if form.is_valid():
            user = request.user
            user_book_id = form.cleaned_data["user_book_id"]
            entry = form.cleaned_data["entry"]

            # load the exact instance of the book in instead of using .filter() which returns a query set
            try:
                user_book = UserBook.objects.get(user=user, id=user_book_id)
            except UserBook.DoesNotExist:
                messages.error(request, "Book does not exist")
                return render(request, "user/friends/requests/request_response.html")

            global_book = user_book.book

            percentage_complete = user_book.next_milestone
            num_milestones = len(user_book.get_milestone_progress())
            points = global_book.point_potential / num_milestones
            points_earned = points

            new_log = ReadingLog(user=user, user_book=user_book, entry=entry, points_earned=points_earned, percentage_complete=percentage_complete)
            new_log.save()

            if user_book.reading_status == "to-read":
                user_book.reading_status = "reading"

            if percentage_complete == 100:
                user_book.reading_status = "read"

                # updates challenge. '__' lets me check if null is true, saving for future use
                if Challenge.objects.filter(Q(player_1=user) | Q(player_2=user), book=global_book, winner__isnull=True, challenge_status="ongoing").exists():
                    challenge = Challenge.objects.get((Q(player_1=user) | Q(player_2=user)), book=global_book)
                    challenge.winner = user
                    challenge.date_finished = datetime.date.today()
                    challenge.challenge_status = "completed"
                    challenge.save()
                    # dunno where to put dis ting 
                    user.profile.bookmarks += challenge.possible_bookmarks
                    user.profile.save()

            user_book.current_progress = percentage_complete
            user_book.save()
            

            user.profile.points += points_earned
            user.profile.entries_made += 1
            user.profile.pages_read += (points_earned / 10)
    
            split_entry = entry.split(" ")
            user.profile.words_written += len(split_entry)

            if user_book.reading_status == "read":
                user.profile.books_read += 1


            user.profile.save()
            messages.success(request, "Entry Saved!")
            return render(request, "user/friends/requests/request_response.html")
        messages.error(request, "Invalid Entry")
        return render(request, "user/friends/requests/request_response.html")   
        
    return render(request, "user/bookshelf/entry_card.html")

            
@login_required
def load_view_entries(request):
    if request.method == "POST":
        form = ViewPastEntries(request.POST)
        if form.is_valid():
            user_book_id = form.cleaned_data["user_book_id"]
            user = request.user

            try:
                user_book = UserBook.objects.get(id=user_book_id, user=user)
                return render(request, "user/bookshelf/view_entries.html", {"user_book": user_book})
            except:
                messages.error(request, "Unable to load entries")
                return render(request, "user/friends/requests/request_response.html")
        

@login_required
def load_past_books(request):
    if request.method == "GET":
        return render(request, "user/bookshelf/past_books.html")
    
@login_required
def book_overview(request):
    return render(request, "books/book_overview.html")

