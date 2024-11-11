from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .serializers import *
from .forms import UserRegistrationForm, DatingProfileForm, LoginForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
#from .forms import *

# Create your views here.
def index(request):
    user =User.objects.all()

    
    data = { "result" :list(user.values())
            }
    return render(request, "homepage.html",data)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        #profile_form = DatingProfileForm(request.POST)
        if user_form.is_valid() :# and profile_form.is_valid():
            user = user_form.save()
            #profile = profile_form.save(commit=False)
            #profile.user = user
            #profile.save()
            DatingProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully. You can now complete your profile.')
            login(request, user)
            return redirect('profile_setup')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistrationForm()
        #profile_form = DatingProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form
        #'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile = DatingProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_setup(request):
    # Get or create the profile for the logged-in user
    profile = request.user.userprofile

    if request.method == 'POST':
        profile_form = DatingProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect to profile page
    else:
        profile_form = DatingProfileForm(instance=profile)

    return render(request, 'profile_setup.html', {
        'profile_form': profile_form
    })



def profilepicture(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'profileupdate.html', {'form': form})