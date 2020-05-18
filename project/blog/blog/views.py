from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

from comment.forms import CommentForm
from comment.models import Comment
from post.forms import PostForm, FilterForm
from post.models import Post
from user.forms import SignUpForm

class HomeView(ListView):
    model = Post
    context_object_name = 'posts' 
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = FilterForm()
        return context

    def get_queryset(self):
        posts = Post.objects.using('PostsAndComments').filter(is_trashed=False).order_by('-last_modified')
        title_query = self.request.GET.get('title')
        user_query = self.request.GET.get('user')
        date_from_query = self.request.GET.get('date_from')
        date_to_query = self.request.GET.get('date_to')

        if title_query != '' and title_query is not None:
            posts = posts.filter(title__icontains=title_query)
        if user_query != '' and user_query is not None:
            posts = posts.filter(user__icontains=user_query)
        if date_from_query != '' and date_from_query is not None:
            posts = posts.filter(last_modified__gte=date_from_query)
        if date_to_query != '' and date_to_query is not None:
            posts = posts.filter(last_modified__lte=date_to_query)

        return posts

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

        current_user = self.request.user.username
        slug = self.kwargs['slug']
        post_user = Post.objects.get(slug=slug).user
        context['is_post_user'] = current_user == post_user

        context['is_superuser']= self.request.user.is_superuser
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse('user_login') + '?next=/' + kwargs['slug'])

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = self.get_object().id
            comment.save(using='PostsAndComments')

            return HttpResponseRedirect(self.request.path_info)
        else:
            return HttpResponse(form.errors) ##todo
            

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = PostForm().fields
    login_url = '/login/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        self.post_instance = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = PostForm().fields
    template_name = 'post_edit.html'
    login_url = '/login/'

    def post(self, request, slug):
        if 'delete' in self.request.POST:
            post_delete = Post.objects.get(slug=slug)
            post_delete.is_trashed = True
            post_delete.save()
        return super(PostUpdateView, self).post(request, slug)

    def form_valid(self, form):
        post = form.save(commit=False)
        self.post_instance = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

    def test_func(self):
        current_user = self.request.user.username
        slug = self.kwargs['slug']
        post_user = Post.objects.get(slug=slug).user
        if current_user == post_user or self.request.user.is_superuser:
            return True
        else:
            if self.request.user.is_authenticated:
                raise Http404("You are not the user of this post")
    

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
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        else:
            return reverse('home')
    
class ModeratorView(ListView):
    template_name = 'moderator.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(ModeratorView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.using('PostsAndComments').all()
        context['posts'] = Post.objects.using('PostsAndComments').all()

        return context
