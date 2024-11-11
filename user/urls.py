#from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.viewset import getJson
from . import views

router = routers.DefaultRouter()

urlpatterns = [
        path("homepage/", views.index, name="home"),
        path(r'',include(router.urls)),
        path(r'api/data/', getJson, name='getJson'),
        
        path('register/',views.register, name="register"),
        path('login/', views.login_view, name="login"),
        path('profile/', views.profile, name="profile"),
        path('profile_setup/', views.profile_setup, name='profile_setup'),
        path('profilepicture/', views.profilepicture, name='profilepicture'),
    #    path("update_task/<str:pk>/", views.updateTask, name = "update_task"),
    #    path("delete_task/<str:pk>/",views.deleteTask, name="delete_task")
]