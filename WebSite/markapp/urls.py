from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.getemployeedata),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('registration/', views.user_signup, name='registration')
]