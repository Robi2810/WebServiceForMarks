from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    title = models.CharField(max_length=35)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievement', null=True, blank=True)
    title = models.CharField(max_length=35)
    description = models.TextField(null=True, blank=True)
    weight = models.IntegerField(default=0)

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

    def __str__(self):
        return str(self.user)
