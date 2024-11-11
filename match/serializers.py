from rest_framework import serializers
from .models import Match, Message

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['user', 'matched_with', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'timestamp']