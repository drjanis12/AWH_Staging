from django import forms
from warehouse.models import Rating, Artist, Album, Song

class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate',]

class ArtistForm(forms.ModelForm):
    class Meta:
        model= Artist
        fields = ['name',]
        labels = {'name': 'Artist Name(s)',}


class AlbumForm(forms.ModelForm):
    class Meta:
        model= Album
        fields = ['name',]
        labels = {'name': 'Album Name',}


class SongForm(forms.Form):
    # class Meta:
    #     model = Song
    name = forms.CharField(label= "Song Name", max_length=32, required=True)
    artist = forms.CharField(label= "Artist Name(s)",max_length=32, required=True)
    album = forms.CharField(label= "Album Name",max_length=32, required=True)
