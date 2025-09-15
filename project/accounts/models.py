from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# user profile
class Profile(models.Model):
    # OneToOneField links the user to each instance of the model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(default="avatar.jpg", upload_to="profile_pictures")
    books_read = models.PositiveIntegerField(default=0)
    words_written = models.PositiveIntegerField(default=0)
    entries_made = models.PositiveIntegerField(default=0)
    pages_read = models.PositiveIntegerField(default=0)
    global_rank = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"




