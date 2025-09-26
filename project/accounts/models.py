from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# user profile
class Profile(models.Model):
    # OneToOneField links the user to each instance of the model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    points = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(default="avatar.jpg", upload_to="profile_pictures")
    books_read = models.PositiveIntegerField(default=0)
    words_written = models.PositiveIntegerField(default=0)
    entries_made = models.PositiveIntegerField(default=0)
    pages_read = models.PositiveIntegerField(default=0)
    bookmarks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)





