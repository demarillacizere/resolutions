from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
import datetime as dt
from .models import Post, Profile, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .forms import RegisterForm, PostForm, ProfileUpdateForm, CommentForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = User.objects.get(username=username)
            profile=Profile.objects.create(user=user,email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request,'registration/registration_form.html')

@login_required
def index(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    for post in posts:
        comments = Comment.objects.filter(post=post).all()
        post.comments=comments.count()
        if request.method=='POST' and 'post' in request.POST:
            posted=request.POST.get("post")
            for post in posts:
                if (int(post.id)==int(posted)):
                    post.likes+=1
                    post.save()
            return redirect('index')
    return render(request,'index.html',{'posts':posts})

@login_required
def my_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user).all()
    form=ProfileUpdateForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
    context={
        'form':form,
        'profile':profile,
        'posts':posts,
    }
    return render(request,"my_profile.html",context=context)

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
        return redirect('index')

    else:
        form = PostForm()
    return render(request, 'newpost.html', {"form": form})

@login_required(login_url='/accounts/login/')
def single_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.get_comments_by_post(post_id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = current_user
            new_comment.post = post
            new_comment.save()
            return redirect('single_post',post_id=post_id)
    elif request.method=='POST' and 'post' in request.POST:
        posted=request.POST.get("post")
        if (int(post.id)==int(posted)):
            post.likes+=1
            post.save()
        return redirect('single_post',post_id=post_id)
    else:
        form = CommentForm()
        
    return render(request, 'post.html', {'post':post, 'form':form,'comments':comments})    

def like(request):
    # image = get_object_or_404(Post, id=request.POST.get('image_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = False

    context = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('like.html', context, request=request)
        return JsonResponse({'form': html})