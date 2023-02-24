from django.shortcuts import render
from itertools import chain
from django.shortcuts import render, redirect
from warehouse.models import Artist, Song, Album


def SearchView(request):
    if request.method=='POST':
        searched = request.POST['searched']
        songs = Song.objects.filter(name__icontains=searched)
        artists = Artist.objects.filter(name__icontains=searched)
        albums = Album.objects.filter(name__icontains=searched)

        artist_dict={}
        for song in songs:
            if len(song.artist.all())>1:
                artist_dict[song]=[]
                for artist in song.artist.all():
                    artist_dict[song].append(artist)
            else:
                for artist in song.artist.all():
                    artist_dict[song]=artist

        return render(request,'search/searchresults.html',
        {'searched':searched,
        'songs':songs,
        'artists':artists,
        'artist_dict':artist_dict,
        'albums':albums},)
    else:
        return render(request,'search/searchresults.html',{} )
