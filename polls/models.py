from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    status = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class LikeProfile(models.Model):
    like_user = models.ManyToManyField(User, blank=True, related_name='liked_user')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
    like_status = models.IntegerField(default=0)
    like_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.user.username


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    inner_com = models.ForeignKey('Comment',
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True,
                                      related_name='inner_comment')

    class Meta:
        ordering = ('comment_time',)

    def __str__(self):
        return str(self.id)







