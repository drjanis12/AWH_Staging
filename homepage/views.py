from django.shortcuts import render
from warehouse.models import Artist, Album, Song, Rating



def index(request):
    all_artist_list = Artist.objects.order_by('followers')[:10]
    context = {'all_artist_list': all_artist_list}
    return render(request, 'homepage/home.html', context)
# Create your views here.
