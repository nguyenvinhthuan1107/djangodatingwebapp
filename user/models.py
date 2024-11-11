from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class DatingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    age = models.PositiveIntegerField(blank=True, null=True, default=0)
    bio = models.TextField(max_length=500, blank=True, null=True, default="")
    location = models.CharField(max_length=100, blank=True)
    interests = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_pic.gif')  # Profile picture with a default value

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Matching function
    def match(self, other_profile):
        score = 0

        # Match based on gender
        if self.gender != other_profile.gender:
            score += 5  # No match, so reduce score

        # Match based on age (e.g., within a range of 5 years)
        if abs(self.age - other_profile.age) <= 5:
            score += 3  # Match based on age range
        elif abs(self.age - other_profile.age) <= 10:
            score+=2
        else: 
            score +=1

        # Match based on location
        if self.location == other_profile.location:
            score += 4  # Location match

        # Match based on interests
        common_interests = set(self.interests.split(',')) & set(other_profile.interests.split(','))
        if common_interests:
            score += 2  # Interest match

        return score

    # Function to get the best match
    @staticmethod
    def get_best_match(profile):
        # Get all profiles excluding the given one
        profiles = DatingProfile.objects.exclude(id=profile.id)

        best_match = None
        best_score = 0

        for other_profile in profiles:
            score = profile.match(other_profile)
            if score > best_score:
                best_score = score
                best_match = other_profile

        return best_match, best_score




    
