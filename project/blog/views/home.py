from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from forms.home import FilterForm
from post.models import Post
from .commons import add_login_context, handle_login

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
        posts = Post.objects.filter(is_trashed=False).order_by('-last_modified')
        filtered_posts = self.apply_query_fields(posts)
        return filtered_posts

    def post(self, request):
        if 'logout' in request.POST:
            logout(request)
        elif 'login' in request.POST:
            handle_login(request)
        elif 'signup' in request.POST:
            return HttpResponseRedirect(reverse('user_new'))
        return HttpResponseRedirect(request.path_info)

    def get(self, request):
        if 'moderator' in request.GET:
            return HttpResponseRedirect(reverse('moderator'))
        return super(HomeView, self).get(request)

    # helper functions

    def apply_query_fields(self, posts):
        """ Filters the post by the query fields specified in FilterForm """

        title_query = self.request.GET.get('title')
        user_query = self.request.GET.get('user')
        date_from_query = self.request.GET.get('date_from')
        date_to_query = self.request.GET.get('date_to')

        if title_query != '' and title_query is not None:
            posts = posts.filter(title__icontains=title_query)
        if user_query != '' and user_query is not None:
            posts = posts.filter(user__icontains=user_query)
        if date_from_query != '' and date_from_query is not None:
            posts = posts.filter(last_modified__date__gte=date_from_query)
        if date_to_query != '' and date_to_query is not None:
            posts = posts.filter(last_modified__date__lte=date_to_query)
        
        return posts
