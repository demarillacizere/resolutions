from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models import Q


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture =models.ImageField(upload_to= 'profiles/', blank=True, default='profiles/default.png')
    bio = models.CharField(max_length=500, default='No bio')
    email=models.EmailField(default='No email')
    contact = models.CharField(max_length=80)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_bio(cls,id, bio):
        update_profile = cls.objects.filter(id = id).update(bio = bio)
        return update_profile

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile
    @classmethod
    def search_user(cls,user):
        return cls.objects.filter(user__username__icontains=user).all()

class Post(models.Model):
    image = models.ImageField(upload_to='images/', default='')
    goal = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    

    def __str__(self):
        return self.goal
    
    class Meta:
        ordering = ['-date_posted']

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    def total_likes(self):
        return self.likes.count()

    @classmethod
    def search(cls,searchterm):
        search = Goal.objects.filter(Q(description__icontains=searchterm))
        return search


class Comment(models.Model):
    comment= models.CharField(max_length =240)
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()
    
    @classmethod
    def update_comment(cls, id ,comment):
        update = cls.objects.filter(id = id).update(comment = comment)
    
    @classmethod
    def get_comments_by_post(cls, id):
        comments = Comment.objects.filter(post__pk = id)
        return comments
    class Meta:
        ordering = ['-date_posted']