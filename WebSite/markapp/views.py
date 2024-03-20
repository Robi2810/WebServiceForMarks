from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Achievement, Task, CustomGroups
from .forms import ProfileForm, AchievementForm, TaskForm, SignUpForm, ProfileEditForm, GroupForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Profile.objects.create(user=user)
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/reg.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect('userprofile')  # Redirect to profile page after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


@login_required(login_url='login')
def user_profile(request):
    userprofile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    return render(request, 'userprofile.html', {'form': userprofile})


@login_required(login_url='login')
def edit_profile(request):
    userprofile = Profile.objects.get(user=request.user)
    form = ProfileEditForm(instance=userprofile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    return render(request, 'edituserprofile.html', {'form': form})


@login_required(login_url='login')
def achievement_create(request):
    form = AchievementForm()
    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('achievement_list')
    return render(request, 'achievement_form.html', {'form': form})


@login_required(login_url='login')
def task_create(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasklist')
    return render(request, 'task_create.html', {'form': form})


@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})
# Для руководителя выбор ачивки


@login_required(login_url='login')
def create_group(request):
    form = GroupForm
    if request.method == 'POST':
        form = GroupForm(request.POST)
        # print(form)
        print(request.POST.get('name'), request.user, request.POST.get('description'))
        CustomGroups.objects.get_or_create(
            name=request.POST.get('name'),
            created_by=request.user,
            description=request.POST.get('description')
        )
        return redirect('groups')
        # if form.is_valid():
        #     form.save()
        #     # CustomGroups.objects.get_or_create(
        #     #     name=request.POST.get('name'),
        #     #     created_by=request.user,
        #     #     description=request.POST.get('description')
        #     # )
        #     print(request.POST.get('name'),request.user, request.POST.get('description'))
        #     return redirect('tasklist')
    return render(request, 'create_group.html', {'group': form})


@login_required(login_url='login')
def group_view(request):
    user_group = CustomGroups.objects.filter(created_by=request.user)
    return render(request, 'group_view.html', {'usergroup': user_group})


@login_required(login_url='login')
def edit_group(request):
    group = CustomGroups.objects.filter(created_by=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('description')
        users = request.POST.get('users')

