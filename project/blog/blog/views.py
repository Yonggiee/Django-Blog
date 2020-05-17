from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from comment.forms import CommentForm
from comment.models import Comment
from post.forms import PostForm
from post.models import Post

class HomeView(ListView):
    model = Post
    context_object_name = 'posts' 
    queryset = Post.objects.using('PostsAndComments').all().order_by('-last_modified')
    template_name = 'home.html'

class PostDetailedView(DetailView):
    model = Post
    template_name='post_detailed.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(PostDetailedView, self).get_context_data(**kwargs) # get the default context data
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
        return super().form_valid(form)  # you need to return the super call

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

class PostUpdateView(UpdateView):
    model = Post
    fields = PostForm().fields
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        self.post_instance = post
        return super().form_valid(form)  # you need to return the super call

    def get_success_url(self):
        return self.post_instance.get_absolute_url()
