
# Create your models here.
from django.db import models
from user.models import DatingProfile

class Match(models.Model):
    user = models.ForeignKey(DatingProfile, related_name='matches', on_delete=models.CASCADE)
    matched_with = models.ForeignKey(DatingProfile, related_name='matched_with', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(DatingProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(DatingProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content}"
    
class LikeDislike(models.Model):
    # The user who likes or dislikes another user
    from_user = models.ForeignKey(DatingProfile, related_name='from_user', on_delete=models.CASCADE)
    # The user being liked or disliked
    to_user = models.ForeignKey(DatingProfile, related_name='to_user', on_delete=models.CASCADE)
    # A boolean to track like or dislike
    is_liked = models.BooleanField(default=False)  # True for like, False for dislike
    # Timestamp when the like/dislike occurred
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # Ensure each pair only has one like/dislike record

    def __str__(self):
        return f"{self.from_user.username} {'liked' if self.is_liked else 'disliked'} {self.to_user.username}"