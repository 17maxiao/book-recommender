from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class ShelfEntry(models.Model): ## this is for book reviews for a particular user 
    title = models.CharField(max_length=200)
    #author = models.CharField(max_length=200)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    #genre = models.CharField(max_length=200)

    def __str__(self):
        return self.title, self.rating


