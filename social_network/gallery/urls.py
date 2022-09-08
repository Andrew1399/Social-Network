from django.urls import path
from gallery.views import ImageView, DownloadView
app_name = 'gallery'

urlpatterns = [
    path('', ImageView.as_view(), name='gallery'),
    path('download/', DownloadView.as_view(), name='download'),
]