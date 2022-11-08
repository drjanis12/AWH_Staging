from django.urls import path

from . import views

app_name= 'warehouse'

urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('<int:artist_id>/', views.ListSongByArtist, name='listsongbyartist'),
    path('detail/<int:song_id>', views.SongDetailView, name='SongDetail'),

]
