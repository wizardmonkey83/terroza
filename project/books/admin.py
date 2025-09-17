from django.contrib import admin
from .models import Book, ReadingLog

# Register your models here.
admin.site.register(Book)
admin.site.register(ReadingLog)