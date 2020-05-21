from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import Http404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from forms.comment import CommentForm
from forms.post import PostForm, MultipleUploadForm
from comment.models import Comment
from post.models import Post
from .commons import add_login_context, handle_login

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
        self.past_context = context
        return context
    
    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
        elif 'login' in request.POST:
            handle_login(request)
        elif 'signup' in request.POST:
            return HttpResponseRedirect(reverse('user_new'))
        else:
            if request.user.is_anonymous:
                return HttpResponseRedirect(reverse('user_login') + '?next=/' + kwargs['slug'])
            form = CommentForm(request.POST)
            if form.is_valid():
                self.save_comment(request, form)
                return HttpResponseRedirect(request.path_info)
            else:
                context = self.get_current_context(request)
                return render(request, self.template_name, context)
        return HttpResponseRedirect(request.path_info) 
    
    def get(self, request, **kwargs):
        if 'moderator' in request.GET:
            return HttpResponseRedirect(reverse('moderator'))
        return super(PostDetailedView, self).get(request)

    #### helper functions

    def save_comment(self, request, form):
        """ Saves the comment in CommentForm into database """

        comment = form.save(commit=False)
        comment.user = request.user.username
        comment.post_id = self.get_object().id
        comment.save()

    def get_current_context(self, request):
        """ 
        Returns the current context of view. 
        The context includes the errors from CommentForm.
        """

        form = CommentForm(request.POST)
        current_user = request.user.username
        slug = self.kwargs['slug']
        post_user = Post.objects.get(slug=slug).user
        is_post_user = current_user == post_user
        comments = Comment.objects.filter(post=self.get_object().id).order_by('-last_modified')

        return {'comment_form':form, 'post': self.get_object(),
            'is_post_user': is_post_user, 'comments':comments}
        
            
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

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return self.post_instance.get_absolute_url()

    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('home'))
        elif 'multiple' in request.POST:
            self.handle_input_file(request)
            return HttpResponseRedirect(request.path_info) 
        return super(PostCreateView, self).post(request)

    def get(self, request):
        if 'moderator' in request.GET:
            return HttpResponseRedirect(reverse('moderator'))
        return super(PostCreateView, self).get(request)

    ## helper functions

    def handle_input_file(self, request):
        """ 
        Saves the information provided by the excel file into database.
        Adds error if the file is not an excel file
        """

        try:
            excel_file = request.FILES['file']
        except MultiValueDictKeyError:
            raise MultiValueDictKeyError("MultiValueDictKeyError")
        if (str(excel_file).split('.')[-1] == "xls"):
            data = xls_get(excel_file, column_limit=2)['Post']
        elif (str(excel_file).split('.')[-1] == "xlsx"):
            data = xlsx_get(excel_file, column_limit=2)['Post']
        else:
            messages.error(request, "this is not an excel file")
            return
        user = request.user
        return self.save_data(data, user)
        
    def save_data(self, data, user):
        """
        Creates and saves Post instance after validation.
        Adds success and error messages for each row in the excel file.
        """

        row_num = 1
        missing_errors = []
        title_errors = []
        success_message = []
        has_error = False
        
        for row in data:
            if len(row) == 2:
                if row[0] == 'Title':
                    continue
                title = row[0]
                desc = row[1]
                new_post = Post(title=title, user=user, desc=desc)
                try:
                    new_post.full_clean()
                except ValidationError as e:
                        for message in e.messages:
                            messages.error(self.request, "row " + str(row_num) + ": " + message, extra_tags='invalid_data')
                        has_error = True
                else:
                    messages.success(self.request, "row " + str(row_num) + ": " + title + " saved successfully")
                    new_post.save()
            else:
                messages.error(self.request, "row " + str(row_num) + ": " + "missing Title/Desc", extra_tags='invalid_data')
            row_num = row_num + 1
        

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
            slug = self.kwargs['slug']
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
        """ Tests if the user is a superuser or the author of the post """

        current_user = self.request.user.username
        slug = self.kwargs['slug']
        post_user = Post.objects.get(slug=slug).user
        if current_user == post_user or self.request.user.is_superuser:
            return True
        else:
            if self.request.user.is_authenticated:
                raise Http404("You are not the user of this post")
