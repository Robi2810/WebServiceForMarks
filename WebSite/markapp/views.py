from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Department, Group, Section, Instructor, GroupInstructor, Emploeye, EmploeyeSection
from .forms import UserCreationForm, LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logoutpage(request):
    logout(request)
    return redirect('/')


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/reg.html', {'form': form})
