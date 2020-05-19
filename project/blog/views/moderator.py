from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView

from forms.moderator import ModeratorFilterForm
from post.models import Post
from .commons import add_login_context

class ModeratorView(ListView):
    template_name = 'moderator.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(ModeratorView, self).get_context_data(**kwargs)
        context = add_login_context(context)
        context['form'] = ModeratorFilterForm()

        title_query = self.request.GET.get('title')
        user_query = self.request.GET.get('user')
        date_from_day_query = self.request.GET.get('date_from_day')
        date_from_month_query = self.request.GET.get('date_from_month')
        date_from_year_query = self.request.GET.get('date_from_year')
        date_to_day_query = self.request.GET.get('date_to_day')
        date_to_month_query = self.request.GET.get('date_to_month')
        date_to_year_query = self.request.GET.get('date_to_year')
        is_deleted_query = self.request.GET.get('is_deleted')
    
        to_search_query = self.request.GET.get('to_search')

        if to_search_query == '1':
            comments = Comment.objects.using('PostsAndComments').all().order_by('-last_modified')

            if title_query != '' and title_query is not None:
                comments = comments.filter(post__title__icontains=title_query)
            if user_query != '' and user_query is not None:
                comments = comments.filter(user__icontains=user_query)
            if date_from_day_query != '' and date_from_day_query is not None:
                posts = posts.filter(last_modified__date__gte=date_from_day_query)
            if date_from_month_query != '' and date_from_month_query is not None:
                posts = posts.filter(last_modified__month__gte=date_from_month_query)
            if date_from_year_query != '' and date_from_year_query is not None:
                posts = posts.filter(last_modified__year__gte=date_from_year_query)
            if date_to_day_query != '' and date_to_day_query is not None:
                posts = posts.filter(last_modified__date__lte=date_to_day_query)
            if date_to_month_query != '' and date_to_month_query is not None:
                posts = posts.filter(last_modified__month__lte=date_to_month_query)
            if date_to_year_query != '' and date_to_year_query is not None:
                posts = posts.filter(last_modified__year__lte=date_to_year_query)
            if is_deleted_query != '' and is_deleted_query is not None:
                comments = comments.filter(is_trashed=is_deleted_query)
            else:
                comments = comments.filter(is_trashed=False)

            context['comments'] = comments

        else:
            posts = Post.objects.using('PostsAndComments').all().order_by('-last_modified')

            if title_query != '' and title_query is not None:
                posts = posts.filter(title__icontains=title_query)
            if user_query != '' and user_query is not None:
                posts = posts.filter(user__icontains=user_query)
            if date_from_day_query != '' and date_from_day_query is not None:
                posts = posts.filter(last_modified__date__gte=date_from_day_query)
            if date_from_month_query != '' and date_from_month_query is not None:
                posts = posts.filter(last_modified__month__gte=date_from_month_query)
            if date_from_year_query != '' and date_from_year_query is not None:
                posts = posts.filter(last_modified__year__gte=date_from_year_query)
            if date_to_day_query != '' and date_to_day_query is not None:
                posts = posts.filter(last_modified__date__lte=date_to_day_query)
            if date_to_month_query != '' and date_to_month_query is not None:
                posts = posts.filter(last_modified__month__lte=date_to_month_query)
            if date_to_year_query != '' and date_to_year_query is not None:
                posts = posts.filter(last_modified__year__lte=date_to_year_query)
            if is_deleted_query != '' and is_deleted_query is not None:
                posts = posts.filter(is_trashed=is_deleted_query)
            else:
                posts = posts.filter(is_trashed=False)

            context['posts'] = posts

        return context