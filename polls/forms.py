from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'city', 'bio', 'status')

    # def save(self, commit=True):
    #     instance = super(ProfileForm, self).save(commit=False)
    #     if commit:
    #         instance.save(update_fields=['name', 'city'])
    #     return instance


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)