from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from comment.forms import CommentForm
from comment.models import Comment
from post.forms import PostForm
from post.models import Post
from user.forms import SignUpForm

class HomeView(ListView):
    model = Post
    context_object_name = 'posts' 
    queryset = Post.objects.using('PostsAndComments').all().order_by('-last_modified')
    template_name = 'home.html'

    def post(self, request):
        if 'logout' in self.request.POST:
            logout(request)
        return HttpResponseRedirect(self.request.path_info)

class PostDetailedView(DetailView):
    model = Post
    template_name='post_detailed.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostDetailedView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.using('PostsAndComments').filter(post=self.get_object().id)
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = self.get_object().id
            comment.save(using='PostsAndComments')

            return HttpResponseRedirect(self.request.path_info)
        else:
            return HttpResponse(form.errors) ##todo

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = PostForm().fields

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        self.post_instance = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

class PostUpdateView(UpdateView):
    model = Post
    fields = PostForm().fields
    template_name = 'post_edit.html'

    def post(self, request, slug):
        if 'delete' in self.request.POST:
            post_delete = Post.objects.get(slug=slug)
            post_delete.is_trashed = True
        return super(PostUpdateView, self).post(request, slug)

    def form_valid(self, form):
        post = form.save(commit=False)
        self.post_instance = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = 'user_new.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        valid = super(UserCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

class UserLoginView(LoginView):
    template_name = 'user_login.html'

    def get_success_url(self):
        if self.kwargs['slug'] != 'home':
            return '/edit/' + self.kwargs['slug']
        return reverse('home')
    
