from django.contrib.auth.models import User, Group
from django.db import models


class CustomGroups(Group):
    created_by = models.ManyToManyField(User, blank=True)  # Removed null=True for ManyToManyField
    description = models.TextField(blank=True, null=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    title = models.CharField(max_length=35)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    current_group = models.ForeignKey(CustomGroups, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=35)
    description = models.TextField(blank=True, null=True)
    weight = models.IntegerField(default=0)
    ach_img = models.ImageField(blank=True, null=True, upload_to='images/achievement/')

    def __str__(self):
        return self.title


class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rank', blank=True, null=True)
    title = models.CharField(max_length=35)
    rank_img = models.ImageField(blank=True, null=True, upload_to='images/rank/')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='images/profile/')
    score = models.IntegerField(default=0)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, null=True, blank=True)  # Adjusted blank=True
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='achievement', null=True, blank=True)

    def __str__(self):
        return str(self.user)
