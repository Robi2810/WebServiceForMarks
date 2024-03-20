from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Achievement, Task, CustomGroups


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'score', 'rank', 'profile_pic']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'weight']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'deadline']


class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroups
        fields = ['name', 'created_by', 'description']

