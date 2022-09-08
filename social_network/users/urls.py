from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.user_profile, name='profile'),
    path('my_invites/', views.invites_received, name='my_invites'),
    path('all_profiles/', views.ProfileListView.as_view(), name='all_profiles'),
    path('<slug>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('available/invites/', views.ProfileInviteListView.as_view(), name='invite_profiles'),
    path('send_invite', views.send_invitation, name='send_invite'),
    path('remove_friend', views.remove_from_friends, name='remove_friend'),
    path('my_invites/accept', views.accept_invitation, name='accept_invitation'),
    path('my_invites/reject', views.reject_invitation, name='reject_invitation'),
]
