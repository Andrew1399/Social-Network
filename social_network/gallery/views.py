from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from gallery.models import Image
from gallery.forms import ImageForm
from users.models import Profile


class ImageView(LoginRequiredMixin, ListView):
    template_name = 'gallery/images.html'
    paginate_by = 3

    def get_queryset(self):
        return Image.objects.filter(author__user=self.request.user).order_by('-datetime')[:100]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = [{
                "path": obj.path_to_image.url,
                "size": obj.size,
                "name": obj.name,
                "time": obj.datetime.strftime("%d %B %Y in %H:%M"),
                "author": obj.author
            } for obj in self.get_queryset()]
        return context


class DownloadView(LoginRequiredMixin, CreateView):
    form_class = ImageForm
    template_name = 'gallery/download.html'
    success_url = '/gallery'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        obj = form.save(commit=False)
        form.instance.author = profile
        form.instance.size = self.request.FILES["path_to_image"].size
        obj.save()
        return super().form_valid(form)
