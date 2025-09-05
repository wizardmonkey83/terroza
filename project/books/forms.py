from django import forms

class BookEntry(forms.Form):
    entry = forms.CharField(label="Your Entry", min_length=350, max_length=700)

class BookQuery(forms.Form):
    query = forms.CharField(label="Your Query", max_length=200)
