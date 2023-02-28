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

        artist_dict_song={}
        for song in songs:
            artist_dict_song[song]=[]
            for artist in song.artist.all():
                artist_dict_song[song].append(artist)

        # artist_dict_album={}
        # for album in albums:
        #     all_song_list= Song.objects.filter(album__id=album.id)
        #     artist_dict_album[album]=[]
        #     for song in all_song_list:


        return render(request,'search/searchresults.html',
        {'searched':searched,
        'songs':songs,
        'artists':artists,
        'artist_dict_song':artist_dict_song,
        'albums':albums},)
    else:
        return render(request,'search/searchresults.html',{} )
