from django.urls import path

from . import views

app_name= 'warehouse'

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('album/<int:album_id>/', views.ListSongByAlbum, name='listsongbyalbum'),
    path('artist/<int:artist_id>/', views.ListSongByArtist, name='listsongbyartist'),
    path('detail/<int:song_id>', views.SongDetailView, name='SongDetail'),

]
