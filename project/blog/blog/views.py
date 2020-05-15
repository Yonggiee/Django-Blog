from django.shortcuts import render
from django.views.generic import ListView
from post.models import Post

def homepage(request):
    posts = Post.objects.using('PostsAndComments').all().order_by('last_modified')
    return render(request, 'home.html', { 'posts':posts })
