from django import forms

class BookEntry(forms.Form):
    book_id = forms.IntegerField()
    entry = forms.CharField(label="Your Entry", min_length=350, max_length=700)

class BookQuery(forms.Form):
    user_query = forms.CharField(label="Your Query", max_length=200)

class AddBook(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    author = forms.CharField(label="Author", max_length=200)
    page_count = forms.IntegerField(label="Pages")
    thumbnail = forms.URLField(label="Cover")
    point_potential = forms.IntegerField(label="Point Potential")

class LoadBookEntry(forms.Form):
    book_id = forms.IntegerField()
