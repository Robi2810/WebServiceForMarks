from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.register, name='registration'),
    path('userprofile/', views.user_profile, name='userprofile'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('tasklist/', views.task_list, name='tasklist'),
    path('taskcreate/', views.create_task, name='taskcreate'),
    path('api/get-group-users/<int:group_id>/', views.get_group_users, name='get_group_users'),
    path('creategroup/', views.create_group,name='creategroup'),
    path('groups/', views.group_view,name='groups'),
    path('groups/<int:group_id>/add-users/', views.add_user_to_group, name='addusertogroup'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/<int:group_id>/tasks/', views.group_tasks, name='group_tasks'),
]
