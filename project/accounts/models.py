from django.db import models

# Create your models here.

# user profile
class UserProfile(models.Model):
    # make sure to include error statements for these in views
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_created = models.DateField()
    image = models.ImageField(upload_to='profile/')

class UserStats(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_points = models.IntegerField()
    rank = models.IntegerField()
    books_read = models.IntegerField()
    chapters_read = models.IntegerField()
    words_written = models.IntegerField()

class UserEntries(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    entry = models.TextField()
    book = models.ForeignKey

