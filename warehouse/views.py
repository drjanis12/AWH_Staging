from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from .models import Artist, Album, Song, Rating
from django.urls import reverse
from django.views import generic
from warehouse.forms import RateForm, SongForm, ArtistForm, AlbumForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def success(request):
    return render(request, 'warehouse/success.html')

def index(request):
    all_artist_list = Artist.objects.order_by('name')
    context = {'all_artist_list': all_artist_list}
    return render(request, 'warehouse/index.html', context)

def ListSongByAlbum(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    all_song_list = Song.objects.filter(album__id=album_id)
    rating_dict = {}
    signin_msg = ''

    if request.user.is_anonymous == False:
        for song in all_song_list:
            if Rating.objects.filter(song=song, user=request.user).values('rate').first() is not None:
                rating_dict[song] = Rating.objects.filter(song=song, user=request.user).values('rate').first()['rate']

    else:
        for song in all_song_list:
            rating_dict[song] = '-'
        signin_msg = 'Please create an account or log in to rate songs and follow artists'

    context = {'album': album,
    'all_song_list': all_song_list,
    'rating_dict': rating_dict,
    'signin_msg': signin_msg}
    #'songs_without_rating': songs_without_rating,}
    return render(request, 'warehouse/listsongbyalbum.html', context)

def ListSongByArtist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    all_song_list = Song.objects.filter(artist__id=artist_id)
    rating_dict = {}
    signin_msg = ''

    if request.user.is_anonymous == False:
        for song in all_song_list:
            if Rating.objects.filter(song=song, user=request.user).values('rate').first() is not None:
                rating_dict[song] = Rating.objects.filter(song=song, user=request.user).values('rate').first()['rate']

        #Follow/Unfollow Artist
        if request.method == "POST":
            current_user = request.user
            action = request.POST['follow']
            if action == 'unfollow':
                current_user.following.remove(artist)
            elif action == 'follow':
                current_user.following.add(artist)
            current_user.save()


    else:
        for song in all_song_list:
            rating_dict[song] = '-'
        signin_msg = 'Please create an account or log in to rate songs and follow artists'

    context = {'artist': artist,
    'all_song_list': all_song_list,
    'rating_dict': rating_dict,
    'signin_msg': signin_msg}
    #'songs_without_rating': songs_without_rating,}
    return render(request, 'warehouse/listsongbyartist.html', context)


def SongDetailView(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    avg_rate = song.average_rating
    if request.user.is_anonymous == False:
        rating_obj = Rating.objects.get_or_create(user=request.user, song=song)
        current_rate= rating_obj[0].rate
        if request.method== 'POST':
            rate_form = RateForm(request.POST, instance=rating_obj[0])
            if rate_form.is_valid():

                save_rate_form = rate_form.save(commit=False)
                save_rate_form.song = song
                save_rate_form.rate = rate_form.cleaned_data.get('rate')
                save_rate_form.user = request.user
                save_rate_form.save()

                messages.success(request, f'Your song has been saved!')
                return redirect('/warehouse/', permanent=True)

        else:
            rate_form = RateForm(instance=Rating())
    else:
        current_rate = '-'
        rate_form = 'Please create account or log in to create user ratings'

    context = {'song' : song,'current_rate': current_rate, 'avg_rate': avg_rate, 'rate_form': rate_form,}
    return render(request, 'warehouse/SongDetail.html', context)

@login_required
def AddSong(request):
    if request.method== 'POST':
        # artist_form = ArtistForm(request.POST, prefix='art', instance=Artist())
        # album_form = AlbumForm(request.POST, instance=Album(), prefix='alb')
        song_form = SongForm(request.POST)
        if song_form.is_valid():
            cleaned_data = song_form.cleaned_data
            #check if artist exists, if not - create new objct
            art_name = cleaned_data.get('artist')
            obj_art = Artist.objects.get_or_create(name=art_name)
            if obj_art[1]=='True':
                obj_art[0].save()

            alb_name = cleaned_data.get('album')
            obj_alb = Album.objects.get_or_create(name=alb_name)
            if obj_alb[1]=='True':
                obj_alb[0].save()

            song_name = cleaned_data.get('name')
            new_song = Song.objects.get_or_create(name=song_name, album=obj_alb[0])
            new_song[0].artist.add(obj_art[0])



            messages.success(request, f'Your song has been saved!')
            return redirect('/', permanent=True)
    else:
        print('song invalid')
        song_form = SongForm()


    context = {
         'song_form': song_form,
    }
    return render(request, 'warehouse/addSong.html', context)

# class SongUpdateView(LoginRequiredMixin, UpdateView):
#     model = Song
#     fields = ['name', 'album','artist',]


class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song
    success_url = '/'
