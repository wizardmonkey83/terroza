from django import forms

class SendChallengeRequest(forms.Form):
    friend_id = forms.IntegerField()
    book_id = forms.IntegerField()

class AcceptChallengeRequest(forms.Form):
    request_id = forms.IntegerField()

class RemoveChallengeRequest(forms.Form):
    request_id = forms.IntegerField()

class ViewOpponentsEntries(forms.Form):
    challenge_id = forms.IntegerField()

class ViewPastChallengeEntries(forms.Form):
    challenge_id = forms.IntegerField()

class SearchFriendChallenge(forms.Form):
    query = forms.CharField(required=False)

class SearchBookChallenge(forms.Form):
    query = forms.CharField(required=False)