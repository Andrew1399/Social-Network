from django.urls import path
from music import views

app_name = 'music'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('songs/', views.SongView.as_view(), name='songs'),
    path('album/add/', views.AlbumCreateView.as_view(), name='album-add'),
    path('album/<pk>/update/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/<pk>/favorite/', views.establish_favorite_album, name='album-favorite'),
    path('album/<pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    path('album/<pk>/detail/', views.AlbumDetailVew.as_view(), name='detail'),
    path('song/<pk>/add/', views.SongCreateView.as_view(), name='song-add'),
    path('song/<pk>/<song_id>/update/', views.SongUpdateView.as_view(), name='song-update'),
    path('song/<pk>/<song_id>/favorite/', views.establish_favorite_song, name='song-favorite'),
    path('song/<pk>/<song_id>/delete/', views.SongDeleteView.as_view(), name='song-delete'),
    path('search/', views.SearchListView.as_view(), name='search')
]
