from django.shortcuts import render, redirect
from django.views.generic import ListView
from post.models import Post
from post.forms import PostForm
from django.http.response import HttpResponse

def home(request):
    posts = Post.objects.using('PostsAndComments').all().order_by('-last_modified')
    return render(request, 'home.html', { 'posts':posts })

def detailed(request, slug):
    post = Post.objects.using('PostsAndComments').get(slug=slug)
    return render(request, 'post_detailed.html', { 'post':post })

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