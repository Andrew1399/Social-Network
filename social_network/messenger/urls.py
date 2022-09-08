from django.urls import path
from messenger import views

app_name = 'messenger'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('new/', views.new, name='new_message'),
    path('send/', views.send, name='send_message'),
    path('users/', views.users, name='users_message'),
    path('<username>/', views.messages, name='messages')
]
