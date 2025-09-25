from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import Profile, FriendRequest
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, SendFriendRequest, AcceptFriendRequest, RemoveFriend, RemoveFriendRequest

from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# LOGIN/SIGN UP
def signup_view(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # creates instance of User class and creates an individual user
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
        


# MANAGING FRIENDSIPS 
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
                    messages.error(request, f"That lonely? Cannot send a request to yourself :)")
                    return render(request, "user/friends/requests/request_response.html")
                
                # so that there arent duplicate requests
                # cooked ahh query 
                if FriendRequest.objects.filter(Q(from_user=from_user, to_user=to_user) | Q(from_user=to_user, to_user=from_user)).exists():
                    messages.error(request, f"Friend request already exists")
                    return render(request, "user/friends/requests/request_response.html")
                
                FriendRequest.objects.create(from_user=from_user, to_user=to_user)
                messages.success(request, "Request Sent!")
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
            friend_request = FriendRequest.objects.get(id=request_id)

            if friend_request.to_user == request.user:
                friend_request.to_user.profile.friends.add(friend_request.from_user)
                friend_request.from_user.profile.friends.add(friend_request.to_user)
                friend_request.delete()
                messages.success(request, f"{friend_request.from_user} is now your friend!")
                return render(request, "user/friends/requests/request_response.html")
            else:
                messages.error(request, "Unable to complete request")
                return render(request, "user/friends/requests/request_response.html")
    
    return render()

@login_required
def remove_friend(request):

    if request.method == "POST":
        form = RemoveFriend(request.POST)
        if form.is_valid():

            try:
                user = request.user
                username = form.cleaned_data["username"] 

                # dont need to use .objects before get since we're already inside the users' friends list
                # pulls up the entire user instance of the friend, so anything related to the friend can be queried
                friend_to_remove = user.profile.friends.get(username=username)
                
                user.profile.friends.remove(friend_to_remove)
                # use .remove() to delete the friend instead of .delete() which removes the user related to the friend
                friend_to_remove.profile.friends.remove(user)
                messages.success(request, f"{friend_to_remove.username} is no longer your friend :(")
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
            friend_request = FriendRequest.objects.get(id=request_id)

            if friend_request.from_user == request.user or friend_request.to_user == request.user:
                if friend_request:
                    friend_request.delete()
                    messages.success(request, f"Request successfully removed!")
                    return render(request, "user/friends/requests/request_response.html")
                else:
                    messages.error(request, f"Unable to remove request")
                    return render(request, "user/friends/requests/request_response.html")
            else:
                messages.error(request, f"Unable to remove request")
                return render(request, "user/friends/requests/request_response.html")
    

# ROUTING STUFF
@login_required
def friends_list(request):
    if request.method == "GET":
        user = request.user
        friends = user.profile.friends.all()
        return render(request, "user/friends/friends.html", {"friends": friends})
    return render(request, "user/friends/friends.html")


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
            pending_requests = FriendRequest.objects.filter(to_user=user)
            return render(request, "user/friends/requests/pending_requests.html", {"pending_requests": pending_requests})
        except:
            messages.error(request, "Error loading requests")
            return render(request, "user/friends/requests/request_response.html")
    return render(request, "user/friends/friends.html")



                

                