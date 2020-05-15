from django.shortcuts import render
from django.views.generic import ListView
from post.models import Post

def home(request):
    posts = Post.objects.using('PostsAndComments').all().order_by('last_modified')
    return render(request, 'home.html', { 'posts':posts })

def detailed(request, slug):
    post = Post.objects.using('PostsAndComments').get(slug=slug)
    return render(request, 'post_detailed.html', { 'post':post })