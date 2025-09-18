from django import forms

class SearchLeaderboard(forms.Form):
    query = forms.CharField(max_length=200)
