from django import forms

class BookEntry(forms.Form):
    entry = forms.CharField(label="Your Entry", min_length=350, max_length=700)

class BookQuery(forms.Form):
    user_query = forms.CharField(label="Your Query", max_length=200)

class AddBook(forms.Form):
    title = forms.CharField(label="Title")
