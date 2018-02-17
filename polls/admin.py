from django.contrib import admin
from .models import Profile, LikeProfile, Comment

admin.site.register(Profile)
admin.site.register(LikeProfile)
admin.site.register(Comment)

