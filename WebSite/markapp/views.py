from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Profile, Achievement, Task, GroupProfile, User, Group
from .forms import ProfileForm, AchievementForm, TaskForm, SignUpForm, ProfileEditForm, GroupProfileForm,\
    GroupCreationForm, AddUsersToGroupForm


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
    usergroups = request.user.groups.all()
    user_achievements = userprofile.achievement.all()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    else:
        form = ProfileForm(instance=userprofile)
    return render(request, 'userprofile.html', {'form': userprofile,
                                                'user_groups': usergroups, 'user_achievements': user_achievements})


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
def create_achievement(request, group_id):
    group_profile = get_object_or_404(GroupProfile, id=group_id, creator=request.user)
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            new_achievement = form.save(commit=False)
            new_achievement.current_group = group_profile
            new_achievement.save()
            return redirect('achievement_list')
    else:
        form = AchievementForm()

    return render(request, 'achievement_create.html', {'form': form})


@login_required(login_url='login')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return redirect('group_tasks', group_id=task.current_group.id)
    else:
        form = TaskForm(user=request.user)
        user_groups = GroupProfile.objects.filter(creator=request.user)
        form.fields['current_group'].queryset = user_groups

    return render(request, 'task_create.html', {'form': form})


def get_group_users(request, group_id):
    group_profile = get_object_or_404(GroupProfile, id=group_id)
    users = list(group_profile.group.user_set.values('id', 'username'))
    return JsonResponse(users, safe=False)


@login_required(login_url='login')
def group_tasks(request, group_id):
    group_profile = get_object_or_404(GroupProfile, id=group_id)
    tasks = Task.objects.filter(current_group=group_profile)
    achievements = Achievement.objects.filter(current_group=group_profile)
    return render(request, 'group_tasks.html', {'group_profile': group_profile, 'tasks': tasks, 'achievements': achievements})


@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})
# Для руководителя выбор ачивки


@login_required(login_url='login')
def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            new_group = form.save()
            user_email = form.cleaned_data.get('user_email')
            if user_email:
                user = User.objects.get(email=user_email)
                new_group.user_set.add(user)

            GroupProfile.objects.create(group=new_group, creator=request.user)

            return redirect('groups')
    else:
        form = GroupCreationForm()

    return render(request, 'create_group.html', {'form': form})


@login_required(login_url='login')
def group_view(request):
    user_groups = GroupProfile.objects.filter(creator=request.user)
    return render(request, 'group_view.html', {'user_groups': user_groups})


@login_required(login_url='login')
def add_user_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)

    if request.method == 'POST':
        form = AddUsersToGroupForm(request.POST)
        if form.is_valid():
            users = form.cleaned_data.get('emails')
            for user in users:
                group.user_set.add(user)
            return redirect('groups')
    else:
        form = AddUsersToGroupForm()

    context = {'form': form, 'group': group}
    return render(request, 'addusertogroup.html', context)


@login_required(login_url='login')
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user.has_perm('auth.delete_group') or group.profile.creator == request.user:
        group.delete()
        return redirect('groups')
    else:

        return redirect('groups')


@login_required(login_url='login')
def achievement_list(request):
    # Achievements obtained by completing tasks
    completed_task_achievements = Achievement.objects.filter(
        task_achievement__user=request.user,
        task_achievement__complete=True
    ).distinct()

    # Achievements created for groups where the user is the creator
    created_group_achievements = Achievement.objects.filter(
        current_group__creator=request.user
    ).distinct()

    # Combine all unique achievements
    all_achievements = (completed_task_achievements | created_group_achievements).distinct()

    return render(request, 'achievement_list.html', {'achievements': all_achievements})


@login_required
def bulk_assign_achievements(request, group_id):
    if request.method == 'POST':
        group_profile = get_object_or_404(GroupProfile, id=group_id, creator=request.user)
        for key, value in request.POST.items():
            if key.startswith('achievement_'):
                task_id = key.split('_')[1]
                achievement_id = value
                task = Task.objects.get(id=task_id, current_group=group_profile)
                if achievement_id:
                    achievement = Achievement.objects.get(id=achievement_id)
                    task.achievement = achievement
                    if task.user:
                        user_profil = Profile.objects.get(user=task.user)
                        user_profil.achievement.add(achievement)
                        user_profil.score += achievement.weight
                        user_profil.save()
                else:
                    task.achievement = None
                task.save()
        return redirect('group_tasks', group_id=group_id)
    # Add else condition for GET request or error handling
