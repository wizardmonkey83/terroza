from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import requests
import os
from dotenv import load_dotenv

# Create your views here.
from .forms import BookEntry, BookQuery, AddBook
from .models import ReadingLog, Book

def search_books(request):

    if request.method == "POST":
        form = BookQuery(request.POST)
        if form.is_valid():
            
            # gets the user"s query from the frontend and formats it so its ready to be ingested by google books 
            user_query = form.cleaned_data["user_query"]
            formatted_user_query = user_query.replace(" ", "+")

            # performs the api search and returns a json reponse with the fields --> authors, page count, title, published date, and front cover
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q={formatted_user_query}&fields=items(volumeInfo(authors,pageCount,title,publishedDate,imageLinks/thumbnail))&key=AIzaSyCsaOh4ZMAGAlansezPtnnxNNy2uhSYhnk"
            response = requests.get(google_books_api_url)
            data = response.json()
            
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

                book = Book.objects.create(user=user, title=title, author=author, cover_image=thumbnail, page_count=page_count, point_potential=point_potential, reading_status="reading")
                book.save()
                # figure out how to replace the card with a "book added" card
                return render(request, "books/book_added_successfully.html", {"title": title})
            
            else:
                print("FORM IS INVALID") 
                print(form.errors)
            
        return render(request, "books/search_books.html")





def save_book_entry(request):
    # if this is a POST request to the backend
    if request.method == "POST":
        # create an instance of the form BookEntry and populate it with the data from the request (the users entry)
        form = BookEntry(request.POST)
        # check to see if the form is valid (if the user made an entry)
        if form.is_valid():
            
            entry = form.cleaned_data["entry"]
            rl = ReadingLog(entry=entry)
            rl.save()

            return HttpResponseRedirect("entry_success/")
        else:
            form = BookEntry()
        
        return
        



