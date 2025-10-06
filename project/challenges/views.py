from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Challenge, ChallengeRequest
from .forms import SendChallengeRequest, AcceptChallengeRequest, RemoveChallengeRequest, ViewOpponentsEntries, ViewPastChallengeEntries, SearchFriendChallenge, SearchBookChallenge
from books.models import Book, UserBook, ReadingLog

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


# ALL ABOUT REQUESTS
@login_required
def send_challenge_request(request):
    if request.method == "POST":
        form = SendChallengeRequest(request.POST)
        if form.is_valid():

            book_id = form.cleaned_data["book_id"]
            friend_id = form.cleaned_data["friend_id"]
            from_user = request.user

            # user exists?
            try: 
                to_user = User.objects.get(id=friend_id)
            except User.DoesNotExist:
                messages.error(request, f"User '{to_user.username}' does not exist")
                return render(request, "user/friends/requests/request_response.html")

            # user holds book?
            try:
                book = Book.objects.get(id=book_id)
                has_book = UserBook.objects.get(user=from_user, book=book)
            except Book.DoesNotExist:
                messages.error(request, "You do not have that book on your shelf")
                return render(request, "user/friends/requests/request_response.html")

            # cmon now
            if to_user == from_user:
                messages.error(request, f"That lonely?")
                return render(request, "user/friends/requests/request_response.html")
        
            # challenge request exists?
            if ChallengeRequest.objects.filter(Q(from_user=from_user, to_user=to_user, book=book) | Q(from_user=to_user, to_user=from_user, book=book)).exists():
                messages.error(request, "Challenge request already exists")
                return render(request, "user/friends/requests/request_response.html")
            
            # challenge currently ongoing?
            if Challenge.objects.filter(Q(player_1=from_user, player_2=to_user, book=book, challenge_status="ongoing") | Q(player_1=to_user, player_2=from_user, book=book, challenge_status="ongoing")).exists():
                messages.error(request, "Challenge already exists")
                return render(request, "user/friends/requests/request_response.html")
            
            # is friended?
            try:
                from_user.profile.friends.get(id=to_user.id)
                ChallengeRequest.objects.create(from_user=from_user, to_user=to_user, book=book)

                messages.success(request, "Challenge request sent!")
                return render(request, "user/friends/requests/request_response.html")

            except User.DoesNotExist:
                messages.error(request, "You can only send challenge requests to friends.")
                return render(request, "user/friends/requests/request_response.html")
        
        messages.error(request, "Invalid Form")
        return render(request, "user/friends/requests/request_response.html")

    messages.error(request, "Invalid Request Method")
    return render(request, "user/friends/requests/request_response.html")


@login_required
def accept_challenge_request(request):

    if request.method == "POST":
        form = AcceptChallengeRequest(request.POST)
        if form.is_valid():

            request_id = form.cleaned_data["request_id"]
            user = request.user

            try:
                challenge_request = ChallengeRequest.objects.get(id=request_id)

            except ChallengeRequest.DoesNotExist:
                messages.error(request, "Unable to complete request")
                return render(request, "user/friends/requests/request_response.html")
            
            if challenge_request.to_user != user:
                messages.error(request, "Unable to accept challenge")
                return render(request, "users/friends/requests/request_response.html")

            
            book_in_challenge = challenge_request.book
            find_or_create_book, created = UserBook.objects.get_or_create(user=user, book=book_in_challenge)
            

            possible_bookmarks = 1
            new_challenge = Challenge(player_1=challenge_request.from_user, player_2=user, book=book_in_challenge, possible_bookmarks=possible_bookmarks, challenge_status="ongoing")
            new_challenge.save()

            challenge_request.delete()

            messages.success(request, "Challenge Accepted!")
            return render(request, "user/friends/requests/request_response.html")
            
@login_required
def remove_challenge_request(request):

    if request.method == "POST":
        form = RemoveChallengeRequest(request.POST)
        if form.is_valid():

            user = request.user
            request_id = form.cleaned_data["request_id"]

            try:
                request_to_remove = ChallengeRequest.objects.get(id=request_id)
                if request_to_remove.from_user == user or request_to_remove.to_user == user:
                    request_to_remove.delete()
                    messages.success(request, "Request Removed!")
                    return render(request, "user/friends/requests/request_response.html")
                
            except ChallengeRequest.DoesNotExist:
                messages.error(request, "Unable to remove request")
                return render(request, "user/friends/requests/request_response.html")
            
            

            


# LOADING PAGES --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def load_send_challenge_request(request):
    if request.method == "GET":
            user = request.user
            # no try-except needed cause if theres no books an empty list will be returned
            to_read_books = UserBook.objects.filter(user=user, reading_status="to-read")
            return render(request, "user/challenges/send_challenge_request.html", {"books": to_read_books})
    
    return render(request, "user/challenges/challenges.html")

@login_required
def load_challenge_page(request):
    if request.method == "GET":
        user = request.user

        try:
            current_challenges = Challenge.objects.filter(Q(player_1=user) | Q(player_2=user), challenge_status="ongoing")
            return render(request, "user/challenges/challenges.html", {"current_challenges": current_challenges})
        except  Challenge.DoesNotExist:
            messages.error(request, "No active challenges")
            return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/challenges/challenges.html")
        

@login_required
def load_past_challenges(request):
    if request.method == "GET":
        user = request.user

        try:
            past_challenges = Challenge.objects.filter(Q(player_1=user) | Q(player_2=user), challenge_status="completed")
            return render(request, "user/challenges/past_challenges.html", {"past_challenges": past_challenges})
        except Challenge.DoesNotExist:
            messages.error(request, "No past challenges.")
            return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/challenges/challenges.html")


@login_required
def load_pending_challenge_requests(request):
    if request.method == "GET":
        user = request.user
        try:
            pending_sent_requests = ChallengeRequest.objects.filter(from_user=user)
            pending_recieved_requests = ChallengeRequest.objects.filter(to_user=user)
            return render(request, "user/challenges/pending_challenge_requests.html", {"pending_sent_requests": pending_sent_requests, "pending_recieved_requests": pending_recieved_requests})

        except ChallengeRequest.DoesNotExist:
            messages.error(request, "No pending requests.")
            return render(request, "user/friends/requests/request_response.html")

    return render(request, "user/challenges/challenges.html")

@login_required
def load_challenge_overview(request):
    return render(request, "user/challenges/challenge_overview.html")


@login_required
def view_opponents_entries(request):
    if request.method == "POST":
        form = ViewOpponentsEntries(request.POST)
        if form.is_valid():

            challenge_id = form.cleaned_data["challenge_id"]
            user = request.user

            try:
                challenge = Challenge.objects.get(id=challenge_id)
                if user == challenge.player_1:
                    user_book = UserBook.objects.get(book=challenge.book, user=challenge.player_2)
                    return render(request, "user/bookshelf/view_entries.html", {"user_book": user_book})
                elif user == challenge.player_2:
                    user_book = UserBook.objects.get(book=challenge.book, user=challenge.player_1)
                    return render(request, "user/bookshelf/view_entries.html", {"user_book": user_book})
            except:
                messages.error(request, "Unable to load entries")
                return render(request, "user/friends/requests/request_response.html")
            
@login_required
def view_past_challenge_entries(request):
    if request.method == "POST":
        form = ViewPastChallengeEntries(request.POST)
        if form.is_valid():

            challenge_id = form.cleaned_data["challenge_id"]
            user = request.user

            try:
                challenge = Challenge.objects.get(id=challenge_id)
                
                user_book = UserBook.objects.get(book=challenge.book, user=user)
                return render(request, "user/bookshelf/view_entries.html", {"user_book": user_book})
            except UserBook.DoesNotExist:
                messages.error(request, f"You no longer have {challenge.book.title} on your bookshelf")
                return render(request, "user/friends/requests/request_response.html")
            
@login_required
def search_challenge_friends(request):
    if request.method == "POST":
        form = SearchFriendChallenge(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            user = request.user

            friends = user.profile.friends.filter(username__icontains=query)
            return render(request, 'user/challenges/friend_list_partial.html', {'friends': friends})
    # so that htmx has something to swap in if the query comes up blank
    return HttpResponse("")
        
@login_required
def search_challenge_books(request):
    if request.method == "POST":
        form = SearchBookChallenge(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            user = request.user
            books = UserBook.objects.filter(user=request.user, reading_status="to-read", book__title__icontains=query)
            return render(request, 'user/challenges/book_list_partial.html', {'books': books})
        
    return HttpResponse("")