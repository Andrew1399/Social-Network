from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.create_post_comment, name='main'),
    path('like_post/', views.like_unlike_post, name='like_post'),
    path('delete/<pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<pk>', views.PostUpdateView.as_view(), name='post_update'),
]
