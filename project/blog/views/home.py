from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from post.forms import FilterForm
from post.models import Post
from .commons import add_login_context

class HomeView(ListView):
    model = Post
    context_object_name = 'posts' 
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context = add_login_context(context)
        context['filter_form'] = FilterForm()
        return context

    def get_queryset(self):
        posts = Post.objects.using('PostsAndComments').filter(is_trashed=False).order_by('-last_modified')
        filtered_posts = self.apply_query_fields(posts)
        return filtered_posts

    def post(self, request):
        if 'logout' in self.request.POST:
            logout(request)
        elif 'login' in self.request.POST:
            username = request.POST['username']
            password = request.POST['password']
            new_user = authenticate(username=username, password=password)
            login(self.request, new_user)
        elif 'signup' in self.request.POST:
            return HttpResponseRedirect(reverse('user_new'))
        return HttpResponseRedirect(self.request.path_info) 

    # helper functions

    def apply_query_fields(self, posts):
        title_query = self.request.GET.get('title')
        user_query = self.request.GET.get('user')
        date_from_day_query = self.request.GET.get('date_from_day')
        date_from_month_query = self.request.GET.get('date_from_month')
        date_from_year_query = self.request.GET.get('date_from_year')
        date_to_day_query = self.request.GET.get('date_to_day')
        date_to_month_query = self.request.GET.get('date_to_month')
        date_to_year_query = self.request.GET.get('date_to_year')

        if title_query != '' and title_query is not None:
            posts = posts.filter(title__icontains=title_query)
        if user_query != '' and user_query is not None:
            posts = posts.filter(user__icontains=user_query)
        if date_from_day_query != '' and date_from_day_query is not None:
            posts = posts.filter(last_modified__day__gte=date_from_day_query)
        if date_from_month_query != '' and date_from_month_query is not None:
            posts = posts.filter(last_modified__month__gte=date_from_month_query)
        if date_from_year_query != '' and date_from_year_query is not None:
            posts = posts.filter(last_modified__year__gte=date_from_year_query)
        if date_to_day_query != '' and date_to_day_query is not None:
            posts = posts.filter(last_modified__day__lte=date_to_day_query)
        if date_to_month_query != '' and date_to_month_query is not None:
            posts = posts.filter(last_modified__month__lte=date_to_month_query)
        if date_to_year_query != '' and date_to_year_query is not None:
            posts = posts.filter(last_modified__year__lte=date_to_year_query)
        
        return posts
