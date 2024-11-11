# matching/views.py
from rest_framework import generics
from .models import Match, Message, LikeDislike
from .serializers import MatchSerializer, MessageSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login,authenticate
from user.models import DatingProfile
from django.db.models import Count, Q, Max
from django.urls import reverse

class MatchListView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

@login_required
def chatchit(request):
    user_profile = request.user.userprofile # Assumes each User has a related UserProfile
    messages = Message.objects.filter(sender=user_profile) | Message.objects.filter(receiver=user_profile)
    
    messages = messages.order_by('timestamp')  # Optional: Order messages by timestamp
    recent_conversations = (
        Message.objects.filter(
            Q(sender=user_profile) | Q(receiver=user_profile)
        )
        .values('sender', 'receiver')  # Group by sender and receiver
        .annotate(last_message_time=Max('timestamp'))
        .order_by('-last_message_time')
        
    )
    unique_conversations = {}

    # Normalize sender-receiver pair: always store the pair as (min_id, max_id)
    for convo in recent_conversations:
        sender = convo['sender']
        receiver = convo['receiver']

        # Ensure sender is always the smaller ID (min) and receiver the larger (max)
        if sender > receiver:
            sender, receiver = receiver, sender

        # Use the normalized (sender, receiver) as the key
        conversation_key = (sender, receiver)

        # If this pair is already processed, skip it; otherwise, process the message
        if conversation_key not in unique_conversations:
            last_message = Message.objects.filter(
                Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
            ).order_by('-timestamp').first()  # Get the latest message

            if last_message:
                other_user = last_message.sender if last_message.receiver == user_profile else last_message.receiver
                unique_conversations[conversation_key] = {
                    'last_message_time': convo['last_message_time'],
                    'last_message': last_message.content,
                    'other_user': other_user,
                }
            else:
                # If no messages found, handle accordingly
                unique_conversations[conversation_key] = {
                    'last_message_time': convo['last_message_time'],
                    'last_message': 'No messages yet.',
                    'other_user': None,
                }

    # Convert dictionary to list for rendering
    final_conversations = list(unique_conversations.values())

    return render(request, 'chatchit.html',{
        'messages': messages,
        'conversations_with_last_message': final_conversations,
    })

@login_required
def conversation_view(request, receiver_id):
    # Get the other user by their ID
    other_user = get_object_or_404(DatingProfile, id=receiver_id)
    
    # Get the logged-in user
    current_user = request.user.userprofile

    # Filter messages where the logged-in user is either sender or receiver and other user is the opposite
    messages = Message.objects.filter(sender=current_user,receiver=other_user) | Message.objects.filter(sender=other_user , receiver=current_user)
    messages=messages.order_by('timestamp')  # Order by timestamp if needed

    return render(request, 'chat.html', {
        'messages': messages,
        'other_user': other_user
    })


@login_required
def send_message(request):
    # Get the receiver user object from the database using the captured ID
    receiver_id = request.POST.get('receiver_id')
    receiver = DatingProfile.objects.get(id=receiver_id)

    # Handle form submission
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user.userprofile, receiver=receiver, content=content)
        return redirect(reverse('conversation', kwargs={'receiver_id': receiver.id}))

    # Pass the receiver user object to the template to be used in the form
    return render(request, 'chat/send_message.html', {
        'receiver': receiver,
    })

@login_required
def new_message(request):
    # Get the receiver user object from the database using the captured ID
    me = request.user.userprofile
    all_matches = []
    profiles = DatingProfile.objects.exclude(id=me.id)

    for profile in profiles:
        like_dislike = LikeDislike.objects.filter(from_user=me, to_user=profile.user.userprofile).first()
        profile.is_liked_by_current_user = like_dislike and like_dislike.is_liked

        # Check if the other user has liked the current user
        reverse_like_dislike = LikeDislike.objects.filter(from_user=profile.user.userprofile, to_user=me).first()
        profile.is_liked_by_other_user = reverse_like_dislike and reverse_like_dislike.is_liked
        if profile.is_liked_by_current_user and profile.is_liked_by_other_user:
            all_matches.append(profile)
  
    return render(request, "new_message.html",{'profilemessage': all_matches})

    # Handle form submission
@login_required
def match(request):
    # Get the user's dating profile
    myprofile = request.user.userprofile

    # Find the best match and get the score
    
    # You can also pass match scores for all profiles if needed
    all_matches = []
    profiles = DatingProfile.objects.exclude(id=myprofile.id)  # Get all profiles except the current one

    for other_profile in profiles:
        score = myprofile.match(other_profile)
        all_matches.append((other_profile, score))

    all_matches = sorted(all_matches, key=lambda x: x[1], reverse=True)

    for profile in profiles:
        like_dislike = LikeDislike.objects.filter(from_user=request.user.userprofile, to_user=profile.user.userprofile).first()
        profile.is_liked_by_current_user = like_dislike and like_dislike.is_liked

        # Check if the other user has liked the current user
        reverse_like_dislike = LikeDislike.objects.filter(from_user=profile.user.userprofile, to_user=request.user.userprofile).first()
        profile.is_liked_by_other_user = reverse_like_dislike and reverse_like_dislike.is_liked

   
    return render(request, 'match.html', {
        'profile': profiles,
        
        'all_matches': all_matches,
        'myprofile':myprofile,
    })

@login_required
def like_profile(request, profile_id):
    profile = DatingProfile.objects.get(id=profile_id)
    user_profile = request.user.userprofile

    # Check if the user has already liked/disliked this profile
    like_dislike = LikeDislike.objects.filter(from_user=request.user.userprofile, to_user=profile.user.userprofile).first()

    if like_dislike:
        # If there's already a like/dislike, just update the action
        like_dislike.is_liked = True  # User liked this profile
        like_dislike.save()
    else:
        # Create a new like/dislike record
        LikeDislike.objects.create(from_user=request.user.userprofile, to_user=profile.user.userprofile, is_liked=True)

    # Redirect to the next profile or matching page
    return redirect('match')

@login_required
def dislike_profile(request, profile_id):
    profile = DatingProfile.objects.get(id=profile_id)
    user_profile = request.user.userprofile

    # Check if the user has already liked/disliked this profile
    like_dislike = LikeDislike.objects.filter(from_user=request.user.userprofile, to_user=profile.user.userprofile).first()

    if like_dislike:
        # If there's already a like/dislike, just update the action
        like_dislike.is_liked = False  # User disliked this profile
        like_dislike.save()
    else:
        # Create a new like/dislike record
        LikeDislike.objects.create(from_user=request.user.userprofile, to_user=profile.user.userprofile, is_liked=False)

    # Redirect to the next profile or matching page
    return redirect('match')
