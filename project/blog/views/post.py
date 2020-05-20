from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from forms.comment import CommentForm
from forms.post import PostForm, MultipleUploadForm
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
        context['comment_form'] = kwargs.get('comment_form', CommentForm())
        context['comments'] = Comment.objects.filter(post=self.get_object().id).order_by('-last_modified')

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
                comment.user = request.user.username
                comment.post_id = self.get_object().id
                comment.save()

                return HttpResponseRedirect(self.request.path_info)
            else:
                form = CommentForm(request.POST or None)
                current_user = self.request.user.username
                slug = self.kwargs['slug']
                post_user = Post.objects.get(slug=slug).user
                is_post_user = current_user == post_user
                comments = Comment.objects.filter(post=self.get_object().id).order_by('-last_modified')
                is_superuser = self.request.user.is_superuser

                return render(request, self.template_name, {'comment_form':form, 'post': self.get_object(),             'is_post_user': is_post_user, 'is_superuser': is_superuser, 'comments':comments})

        return HttpResponseRedirect(self.request.path_info) 


        
            

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    form_class = PostForm
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['multi_upload'] = MultipleUploadForm()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        self.post_instance = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('home'))
        elif 'multiple' in request.POST:
            self.handle_input_file(request)
            return HttpResponseRedirect(reverse('home'))
        return super(PostCreateView, self).post(request)

    def get(self, request):
        if 'moderator' in request.GET:
            return HttpResponseRedirect(reverse('moderator'))
        return super(PostCreateView, self).get(request)

    ## helper functions

    def handle_input_file(self, request):
        try:
            excel_file = request.FILES['file']
        except MultiValueDictKeyError:
            raise MultiValueDictKeyError("WHAT")
        
        if (str(excel_file).split('.')[-1] == "xls"):
            data = xls_get(excel_file, column_limit=2)['Sheet1']
        elif (str(excel_file).split('.')[-1] == "xlsx"):
            data = xlsx_get(excel_file, column_limit=2)['Sheet1']
        
        user = request.user

        for row in data:
            if row[0] == 'Title':
                continue
            if len(row) == 2:
                if (row[0] != '' or row[0] == None) and (row[1] != '' or row[0] == None):
                    Post.objects.create(user=user, title=row[0], desc=row[1])



class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('home'))
        elif 'delete' in request.POST:
            post_delete = Post.objects.get(slug=slug)
            post_delete.is_trashed = True
            post_delete.save()
            return HttpResponseRedirect(reverse('home'))
        return super(PostUpdateView, self).post(request)
    
    def get(self, request, *args, **kwargs):
        if 'moderator' in request.GET:
            return HttpResponseRedirect(reverse('moderator'))
        return super(PostUpdateView, self).get(request)

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
