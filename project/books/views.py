from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import os
from dotenv import load_dotenv

# Create your views here.
from .forms import BookEntry, BookQuery
from .models import ReadingLog

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(BASE_DIR)

load_dotenv(os.path.join(PROJECT_ROOT, ".gitignore/.env"))

def search_books(request):

    if request.method == "POST":

        form = BookQuery(request.POST)

        if form.is_valid():
            
            # gets the user's query from the frontend and formats it so its ready to be ingested by google books 
            user_query = form.cleaned_data["user_query"]
            formatted_user_query = user_query.replace(" ", "+")

            # performs the api search and returns a json reponse with the fields --> authors, page count, title, published date, and front cover
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q={formatted_user_query}&fields=items(volumeInfo(authors,pageCount,title,publishedDate,imageLinks/thumbnail))&key={api_key}"
            response = requests.get(google_books_api_url)
            data = response.json()
            return data
        


def add_book(requests):
    # if the user presses "add" the books information gets stored to the database and is linked to the user
    




def get_book_entry(request):
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
        

