from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.
class Artist(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Album(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    @property
    def average_rating(self):
        return self.rating_set.all().aggregate(Avg('rate'))['rate__avg']

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])

    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
