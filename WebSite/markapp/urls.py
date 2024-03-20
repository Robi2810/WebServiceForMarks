from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.register, name='registration'),
    path('userprofile/', views.user_profile, name='userprofile'),
    path('editprofile', views.edit_profile, name='editprofile'),
    path('tasklist/', views.task_list, name='tasklist'),
    path('taskcreate/', views.task_create, name='taskcreate'),
    path('creategroup/', views.create_group,name='creategroup'),
    path('groups/', views.group_view,name='groups'),
]
