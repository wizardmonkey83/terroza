from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    STATUS_CHOICES = [
        ("to-read", "To Read"),
        ("reading", "Currently Reading"),
        ("read", "Read"),
    ]

    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200)
    cover_image = models.ImageField()
    page_count = models.PositiveIntegerField()
    point_potential = models.PositiveIntegerField()
    reading_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to-read")

    def __str__(self):
        return self.title

class ReadingLog(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="entries")
    percentage_complete = models.PositiveIntegerField()
    points_earned = models.PositiveIntegerField()
    # set a min length
    entry = models.TextField()
    # automatically sets and is immutable
    date_of_entry = models.DateField(auto_add_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.percentage_complete} Percent Complete"





