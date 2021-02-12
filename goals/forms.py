from django import forms
from .models import Profile, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user','image','likes','comments']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','email']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post', 'user', 'date_posted']