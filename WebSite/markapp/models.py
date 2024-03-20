from django.contrib.auth.models import User, Group
from django.db import models


class CustomGroups(Group):
    created_by = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=35)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    current_group = models.ForeignKey(CustomGroups, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField(null=True, blank=True)
    weight = models.IntegerField(default=0)
    ach_img = models.ImageField(null=True, blank=True, upload_to='images/achievement/')

    def __str__(self):
        return self.title

    def __int__(self):
        return self.weight


class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rank', null=True, blank=True)
    title = models.CharField(max_length=35)
    rank_img = models.ImageField(null=True, blank=True, upload_to='images/rank/')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/')
    score = models.IntegerField(default=0)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, null=True, blank=False)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='achievement', null=True)

    def __str__(self):
        return str(self.user)


# CLASS GROUPS VIEW TASK_LIST HTML