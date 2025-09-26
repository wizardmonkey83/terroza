from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Challenge, ChallengeRequest
from .forms import SendChallengeRequest, AcceptChallengeRequest, RemoveChallengeRequest
from books.models import Book

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


# ALL ABOUT REQUESTS
@login_required
def send_challenge_request(request):
    if request.method == "POST":
        form = SendChallengeRequest(request.POST)
        if form.is_valid():

            book_id = form.cleaned_data["book_id"]
            username = form.cleaned_data["username"]
            from_user = request.user

            try: 
                to_user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, f"User '{username}' does not exist")
                return render(request, "user/friends/requests/request_response.html")

            try:
                book = Book.objects.get(user=from_user, id=book_id)
            except Book.DoesNotExist:
                messages.error(request, "You do not have that book on your shelf")
                return render(request, "user/friends/requests/request_response.html")

            if to_user == from_user:
                messages.error(request, f"That lonely? Cannot send a request to yourself :)")
                return render(request, "user/friends/requests/request_response.html")
        
            if ChallengeRequest.objects.filter(Q(from_user=from_user, to_user=to_user, book=book) | Q(from_user=to_user, to_user=from_user, book=book)).exists():
                messages.error(request, "Challenge request already exists")
                return render(request, "user/friends/requests/request_response.html")
            
            ChallengeRequest.objects.create(from_user=from_user, to_user=to_user, book=book)
            messages.success(request, "Challenge request sent!")
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

            try:
                does_to_user_have_book = user.books.get(id=challenge_request.book.id)

                possible_bookmarks = round(does_to_user_have_book.page_count / 10)
                new_challenge = Challenge(player_1=challenge_request.from_user, player_2=user, book=does_to_user_have_book, possible_bookmarks=possible_bookmarks, challenge_status="ongoing")
                new_challenge.save()

                challenge_request.delete()

                messages.success(request, "Challenge Accepted!")
                return render(request, "user/friends/requests/request_response.html")

            except Book.DoesNotExist:
                messages.error(request, f"Add {challenge_request.book.title} to your bookshelf before proceeding")
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
        return render(request, "user/challenges/requests/send_challenge_request.html")
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

