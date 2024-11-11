# matching/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('conversation/', chatchit, name='chatchit'),
    path('api/messages/',MessageListView.as_view(), name='message-list'),
    path('conversation/<int:receiver_id>/', conversation_view, name='conversation'),
    path('send-message/', send_message, name='send_message'),
    path('new_message/', new_message, name='new_message'),
    path('match/', match, name='match'),
    path('like/<int:profile_id>/', like_profile, name='like_profile'),
    path('dislike/<int:profile_id>/', dislike_profile, name='dislike_profile'),
]
