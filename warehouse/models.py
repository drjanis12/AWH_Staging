from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
# Create your models here.
class Artist(models.Model):
    name= models.CharField(max_length=200)
    followers= models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='following', null=True)

    @property
    def average_rating(self):
        songs_by_artist= Song.objects.filter(artist=self)
        rating_list = [song.average_rating for song in songs_by_artist]
        return round(sum(rating_list)/len(rating_list),2)

    @property
    def rating_count(self):
        songs_by_artist= Song.objects.filter(artist=self)
        rating_list_count = len(Rating.objects.filter(song__in= songs_by_artist))
        return round(rating_list_count,2)

    def __str__(self):
        return self.name

class Album(models.Model):
    name= models.CharField(max_length=200)

    @property
    def average_rating(self):
        songs_in_album= Song.objects.filter(album_id=self.id)
        rating_list = [song.average_rating for song in songs_in_album]
        return round(sum(rating_list)/len(rating_list),2)

    @property
    def rating_count(self):
        songs_in_album= Song.objects.filter(album_id=self.id)
        rating_list_count = len(Rating.objects.filter(song__in= songs_in_album))
        return round(rating_list_count,2)


    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')

    @property
    def average_rating(self):
        return round(self.rating_set.all().aggregate(Avg('rate'))['rate__avg'],2)

    @property
    def user_ratings(self):
        return self.rating_set.filter(song=self, user=request.user)

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
