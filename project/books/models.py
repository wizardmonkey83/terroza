from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    cover_image = models.URLField(max_length=400)
    page_count = models.PositiveIntegerField(default=0)
    point_potential = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class UserBook(models.Model):
    STATUS_CHOICES = [
        ("reading", "Reading"),
        ("to-read", "To-Read"),
        ("read", "Read"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reading_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to-read")

    def __str__(self):
        return f"{self.user.username}'s copy of {self.book.title}"
    
    def get_milestone_progress(self):

        # might be a scuffed method of determining milestones
        if self.book.page_count < 150 and self.book.page_count > 50:
            num_milestones = 2
        elif self.book.page_count < 50:
            num_milestones = 1
        else:
            num_milestones = round(self.page_count / 75)

        # avoid dividing by 0
        num_milestones = max(1, num_milestones)

        increment = 100 / num_milestones
        all_milestones = [round(i * increment) for i in range(1, num_milestones + 1)]

        # 'entries' maps to the reading log instance
        completed_logs = self.logs.all(user=self.user)
        # creates a set
        completed_percentages = set(completed_logs.values_list('percentage_complete', flat=True))

        # so that completed milestones can be tracked
        progress = []
        for milestone in all_milestones:
            progress.append({
                'percentage': milestone,
                'is_complete': milestone in completed_percentages
            })

        return progress

    # '@property' allows function to be referenced
    @property
    def next_milestone(self):
        progress = self.get_milestone_progress()

        for milestone in progress:
            if not milestone['is_complete']:
                return milestone['percentage']
        return None

class ReadingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    user_book = models.ForeignKey(UserBook, on_delete=models.CASCADE, related_name="logs")
    percentage_complete = models.PositiveIntegerField(default=0)
    points_earned = models.PositiveIntegerField()
    # set a min length
    entry = models.TextField()
    date_of_entry = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_book.book.title} - {self.percentage_complete} Percent Complete"





