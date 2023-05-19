from django.urls import path
from . import views
from .views import SongDeleteView
# SongUpdateView

app_name= 'warehouse'

urlpatterns = [
    path('', views.index, name='index'),
    path('song/new/', views.AddSong, name='addSong'),
    # path('song/<int:pk>/update/', SongUpdateView.as_view(), name='song-update'),
    path('song/<int:pk>/delete/', SongDeleteView.as_view(), name='song-delete'),
    path('success/', views.success, name='success'),
    path('album/<int:album_id>/', views.ListSongByAlbum, name='listsongbyalbum'),
    path('artist/<int:artist_id>/', views.ListSongByArtist, name='listsongbyartist'),
    path('detail/<int:song_id>', views.SongDetailView, name='SongDetail'),

]
