from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import Profile, FriendRequest
from challenges.models import Challenge
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, SendFriendRequest, AcceptFriendRequest, RemoveFriend, RemoveFriendRequest

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# LOGIN/SIGN UP ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def signup_view(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            # creates instance of User class and creates an individual user
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, "Username and/or Email already exists")
                return render(request, "user/friends/requests/request_response.html")


            user = form.save()
            # creates profile model alongside the user
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("user_home")
        
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_home")
            
    else:
        form = LoginForm()
    
    return render(request, "registration/login.html", {"form": form})
        
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def delete_account(request):
    user = request.user

    user.delete()
    return redirect("signup")

@login_required
def load_delete_account_caution(request):
    if request.method == "GET":
        return render(request, "registration/delete_account_caution.html")




# MANAGING FRIENDSIPS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def send_friend_request(request):
    
    if request.method == "POST":
        form = SendFriendRequest(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            from_user = request.user

            # no ghost requests
            try:
                to_user = User.objects.get(username=username)

                # so people cant friend themselves
                if to_user == from_user:
                    messages.error(request, "That lonely?")
                    return render(request, "user/friends/requests/request_response.html")

                # already friended?
                if from_user.profile.friends.filter(id=to_user.id).exists():
                    messages.error(request, "Friend already added")
                    return render(request, "user/friends/requests/request_response.html")
                
                # so that there arent duplicate requests
                # cooked ahh query 
                if FriendRequest.objects.filter(Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)).exists():
                    messages.error(request, "Friend request already exists")
                    return render(request, "user/friends/requests/request_response.html")
                
                FriendRequest.objects.create(from_user=from_user, to_user=to_user)
                messages.success(request, "Friend request sent!")
                return render(request, "user/friends/requests/request_response.html")
            
            except User.DoesNotExist:
                messages.error(request, f"User '{username}' does not exist")
                return render(request, "user/friends/requests/request_response.html")
    
@login_required
def accept_friend_request(request):

    if request.method == "POST":
        form = AcceptFriendRequest(request.POST)
        if form.is_valid():

            request_id = form.cleaned_data["request_id"]

            try: 
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.to_user == request.user:
                    friend_request.to_user.profile.friends.add(friend_request.from_user)
                    friend_request.from_user.profile.friends.add(friend_request.to_user)
                    friend_request.delete()
                    messages.success(request, f"{friend_request.from_user} is now your friend!")
                    return render(request, "user/friends/requests/request_response.html")
            except FriendRequest.DoesNotExist:
                messages.error(request, "Unable to complete request")
                return render(request, "user/friends/requests/request_response.html")
            
    
    return render()

@login_required
def remove_friend(request):

    if request.method == "POST":
        form = RemoveFriend(request.POST)
        if form.is_valid():

            user = request.user
            friend_id = form.cleaned_data["friend_id"] 

            try:
                # dont need to use .objects before get since we're already inside the users' friends list
                # pulls up the entire user instance of the friend, so anything related to the friend can be queried
                friend_to_remove = user.profile.friends.get(id=friend_id)
                user.profile.friends.remove(friend_to_remove)
                # use .remove() to delete the friend instead of .delete() which removes the user related to the friend
                friend_to_remove.profile.friends.remove(user)

                if Challenge.objects.filter(Q(player_1=friend_to_remove, player_2=user, challenge_status="ongoing") | Q(player_2=friend_to_remove, player_1=user, challenge_status="ongoing")).exists():
                    Challenge.objects.filter(Q(player_1=friend_to_remove, player_2=user, challenge_status="ongoing") | Q(player_2=friend_to_remove, player_1=user, challenge_status="ongoing")).delete()

                messages.success(request, f"Succesfully unfriended: {friend_to_remove.username}")
                return render(request, "user/friends/requests/request_response.html")
            
            except User.DoesNotExist:
                messages.error(request, "User is not on your friends list.")
                return render(request, "user/friends/requests/request_response.html")
            
        
@login_required
def remove_friend_request(request):

    if request.method == "POST":
        form = RemoveFriendRequest(request.POST)
        if form.is_valid():

            request_id = form.cleaned_data["request_id"]
            try:
                friend_request = FriendRequest.objects.get(id=request_id)

                if friend_request.from_user == request.user or friend_request.to_user == request.user:
                    if friend_request:
                        friend_request.delete()
                        messages.success(request, f"Request successfully removed!")
                        return render(request, "user/friends/requests/request_response.html")
            except:
                messages.error(request, f"Unable to remove request")
                return render(request, "user/friends/requests/request_response.html")

            
    

# ROUTING STUFF
@login_required
def load_send_friend_request(request):
    if request.method == "GET":
        return render(request, "user/friends/requests/send_request.html")
    return render(request, "user/friends/friends.html")


@login_required
def load_pending_requests(request):
    if request.method == "GET":
        user = request.user
        try:
            pending_recieved_requests = FriendRequest.objects.filter(to_user=user)
            pending_sent_requests = FriendRequest.objects.filter(from_user=user)
            return render(request, "user/friends/requests/pending_requests.html", {"pending_recieved_requests": pending_recieved_requests, "pending_sent_requests": pending_sent_requests})
        except:
            messages.error(request, "Error loading requests")
            return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/friends/friends.html")

@login_required
def load_remove_friend_caution(request):
    if request.method == "POST":
        form = RemoveFriend(request.POST)
        if form.is_valid():
            
            friend_id = form.cleaned_data["friend_id"]
            user = request.user

            try:
                friend = user.profile.friends.get(id=friend_id)
                return render(request, "user/friends/requests/you_sure.html", {"friend": friend})
            except:
                messages.error(request, "Unable to Remove Friend")
                return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/friends/friends.html")




                

                