from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):

    # removes help text from form
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    # what to include in the form from the built-in user model
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SendFriendRequest(forms.Form):
    username = forms.CharField(max_length=200)

class AcceptFriendRequest(forms.Form):
    request_id = forms.IntegerField()

class RemoveFriend(forms.Form):
    username = forms.CharField(max_length=200)

class RemoveFriendRequest(forms.Form):
    request_id = forms.IntegerField()