from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Artist, Album, Song, Rating
from django.urls import reverse
from django.views import generic
from warehouse.forms import RateForm

def success(request):
    return render(request, 'warehouse/success.html')

def index(request):
    all_artist_list = Artist.objects.order_by('name')
    context = {'all_artist_list': all_artist_list}
    return render(request, 'warehouse/index.html', context)

def ListSongByArtist(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    all_song_list = Song.objects.filter(artist__id=artist_id)
    context = {'all_song_list': all_song_list,
        'artist': artist,}
    return render(request, 'warehouse/listsongbyartist.html', context)

def SongDetailView(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    avg_rate = song.average_rating
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

    context = {'song' : song,'current_rate': current_rate, 'avg_rate': avg_rate, 'rate_form': rate_form,}
    return render(request, 'warehouse/SongDetail.html', context)

# def Rate(request, song_id):
#     song = get_object_or_404(Song, pk=song_id)






# class SongDetailView(generic.DetailView):
#     model = Song
#     template_name = 'warehouse/SongDetail.html'


# def vote(request, song_id):
#     return HttpResponse("You're voting on song %s." % song_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
