from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('authors/', views.authors, name="authors"),
    path('login/', views.loginuser, name="login"),
    path('follower_count/', views.follower_count, name="follower_count"),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutuser, name="logout"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('create_profile/', views.create_profile, name="create_profile"),
    path('userProfile/<str:pk>/',views.userProfile,name='userProfile'),
    path('authors/', views.authors, name="authors"),
    
]

 