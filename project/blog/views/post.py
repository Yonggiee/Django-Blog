from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from forms.comment import CommentForm
from forms.post import PostForm
from comment.models import Comment
from post.models import Post
from .commons import add_login_context

class PostDetailedView(DetailView):
    model = Post
    template_name='post_detailed.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostDetailedView, self).get_context_data(**kwargs)
        context = add_login_context(context)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.using('PostsAndComments').filter(post=self.get_object().id)

        current_user = self.request.user.username
        slug = self.kwargs['slug']
        post_user = Post.objects.get(slug=slug).user
        context['is_post_user'] = current_user == post_user

        context['is_superuser']= self.request.user.is_superuser
        return context
    
    def post(self, request, *args, **kwargs):
        if 'logout' in self.request.POST:
            logout(request)
        elif 'login' in self.request.POST:
            username = request.POST['username']
            password = request.POST['password']
            new_user = authenticate(username=username, password=password)
            login(self.request, new_user)
        elif 'signup' in self.request.POST:
            return HttpResponseRedirect(reverse('user_new'))
        else:
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

        return HttpResponseRedirect(self.request.path_info) 
            

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = PostForm().fields
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        temp = context['form'].save(commit=False)
        context['form'] = PostForm(instance=temp)
        return context

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

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        temp = context['form'].save(commit=False)
        context['form'] = PostForm(instance=temp)
        return context

    def post(self, request, slug):
        if 'delete' in self.request.POST:
            post_delete = Post.objects.get(slug=slug)
            post_delete.is_trashed = True
            post_delete.save()
            return HttpResponseRedirect(reverse('home'))
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