from django.db import models
from django.contrib.auth.models import User
from books.models import Book, UserBook

# Create your models here.
class ChallengeRequest(models.Model):
    # check to see if the 'on_delete' constraint is correct (doesnt delete all instances of the user or book)
    from_user = models.ForeignKey(User, related_name="from_user_challenges", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user_challenges", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="request_book", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user.username} sent a challenge request to {self.to_user.username}"


class Challenge(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("ongoing", "Ongoing"),
        # for a default value
        ("blank", "Blank"),
    ]
    # check to see if the 'on_delete' constraint is correct (doesnt delete all instances of the user or book)
    # corresponds to 'from_user'
    player_1 = models.ForeignKey(User, related_name="player_1", on_delete=models.CASCADE)
    # corresponds to "to_user"
    player_2 = models.ForeignKey(User, related_name="player_2", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="challenge_book", on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_finished = models.DateField(null=True, blank=True)
    possible_bookmarks = models.PositiveIntegerField(default=0)
    # the correct 'on_delete' constraint?
    winner = models.ForeignKey(User, related_name="winner", on_delete=models.SET_NULL, null=True, blank=True)
    challenge_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="blank")

    def get_player_progress(self, player):
        try:
            user_book = UserBook.objects.get(user=player, book=self.book)
            return user_book.current_progress
        except UserBook.DoesNotExist:
            return 0
        
    @property
    def player_1_progress(self):
        return self.get_player_progress(self.player_1)
    
    @property
    def player_2_progress(self):
        return self.get_player_progress(self.player_2)