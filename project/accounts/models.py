from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# user profile
class Profile(models.Model):
    # OneToOneField links the user to each instance of the model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    books_read_count = models.PositiveIntegerField(default=0)
    words_written_count = models.PositiveIntegerField(default=0)
    entries_made_count = models.PositiveBigIntegerField(default=0)
    global_rank = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.user.username}'s Profile"




