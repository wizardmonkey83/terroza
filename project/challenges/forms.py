from django import forms

class SendChallengeRequest(forms.Form):
    username = forms.CharField(max_length=200)
    book_id = forms.IntegerField()

class AcceptChallengeRequest(forms.Form):
    request_id = forms.IntegerField()

class RescindChallengeRequest(forms.Form):
    request_id = forms.IntegerField()