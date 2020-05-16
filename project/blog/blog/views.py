from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from comment.forms import CommentForm
from comment.models import Comment
from post.forms import PostForm
from post.models import Post

def home(request):
    posts = Post.objects.using('PostsAndComments').all().order_by('-last_modified')
    return render(request, 'home.html', { 'posts':posts })

def detailed(request, slug):

    post = Post.objects.using('PostsAndComments').get(slug=slug)
    comments = Comment.objects.using('PostsAndComments').all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.is_trashed = False
            comment.user = request.user
            comment.post_id = post.id
            comment.save(using='PostsAndComments')
            return redirect('detailed', slug=post.slug)
        else:
            return HttpResponse(form.errors) ##todo
    else:
        comment_form = CommentForm()
        return render(request, 'post_detailed.html', { 'post':post, 'comments':comments, 'form':comment_form })

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_trashed = False
            post.user = request.user
            post.save(using='PostsAndComments')
            return redirect('detailed', slug=post.slug)
        else:
            return HttpResponse(form.errors) ##todo
    else:
        post_form = PostForm()
        return render(request, 'post_new.html', { 'form':post_form })