from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    CreateView, UpdateView,
    DeleteView, ListView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from music.models import Album, Song
from users.models import Profile


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'music/index.html'
    context_object_name = "all_albums"

    def get_queryset(self):
        return Album.objects.filter(user__user=self.request.user)


class SongView(LoginRequiredMixin, ListView):
    template_name = 'music/songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        return Song.objects.all()

class AlbumDetailVew(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'music/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailVew, self).get_context_data(**kwargs)
        context['link_detail'] = True
        context['header_text'] = 'All songs'
        return context

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'artist', 'year', 'logo']

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        obj = form.save(commit=False)
        form.instance.user = profile
        obj.save()
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    template_name = 'music/detail_form.html'
    fields = ['title', 'artist', 'year', 'logo', 'is_favorite']

    def get_context_data(self, **kwargs):
        context = super(AlbumUpdateView, self).get_context_data(**kwargs)
        context['link_album_update'] = True
        context['header_text'] = "Edit album details"
        return context

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

@login_required
def establish_favorite_album(request, **kwargs):
    album = get_object_or_404(Album, pk=kwargs['pk'])
    try:
        album.is_favorite = not album.is_favorite
        album.save()
    except(KeyError, Album.DoesNotExist):
        return HttpResponse('Album not found')

    else:
        return redirect('music:index')

class SongCreateView(LoginRequiredMixin, CreateView):
    model = Song
    template_name = 'music/detail_form.html'
    fields = ['title', 'file', 'track_number', 'is_favorite']

    def get_context_data(self, **kwargs):
        album_number = self.kwargs['pk']
        context = super(SongCreateView, self).get_context_data(**kwargs)
        context['album'] = Album.objects.get(id=album_number)
        context['link_song_create'] = True
        context['header_text'] = 'Add a new song'
        return context

    def form_valid(self, form):
        # profile = Profile.objects.get(user=self.request.user)
        album_number = self.kwargs['pk']
        # form.instance.user = profile
        form.instance.album = Album.objects.get(id=album_number)
        return super(SongCreateView, self).form_valid(form)


class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Song
    pk_url_kwarg = 'song_id'
    template_name = 'music/detail_form.html'
    fields = ['title', 'file', 'track_number', 'is_favorite']

    def get_context_data(self, **kwargs):
        album_number = self.kwargs['pk']
        context = super(SongUpdateView, self).get_context_data(**kwargs)
        context['album'] = Album.objects.get(id=album_number)
        context['link_song_update'] = True
        context['header_text'] = 'Edit song details'
        return context

class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song
    pk_url_kwarg = 'song_id'
    def get_success_url(self):
        return reverse_lazy("music:detail", kwargs={'pk': self.kwargs['pk']})

@login_required
def establish_favorite_song(request, **kwargs):
    song = get_object_or_404(Song, pk=kwargs['pk'])
    try:
        song.is_favorite = not song.is_favorite
        song.save()
    except (KeyError, Song.DoesNotExist):
        return HttpResponse("Song not found.")
    else:
        return redirect('music:detail', pk=kwargs['pk'])

class SearchListView(ListView):
    template_name = "music/search.html"
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            search_results = Song.objects.filter(
                Q(album__artist__icontains=query) |
                Q(album__title__icontains=query) |
                Q(album__year__icontains=query) |
                Q(title__icontains=query)
            )
            return search_results
