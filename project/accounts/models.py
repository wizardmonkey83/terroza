from django.db import models

# Create your models here.

# user profile
class UserProfile(models.Model):
    username = models.CharField(max_length=30)
    date_created = models.DateField()