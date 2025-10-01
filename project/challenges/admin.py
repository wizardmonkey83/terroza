from django.contrib import admin
from .models import Challenge, ChallengeRequest

# Register your models here.
admin.site.register(Challenge)
admin.site.register(ChallengeRequest)