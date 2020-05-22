from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from enum import Enum

from comment.models import Comment
from forms.moderator import ModeratorFilterForm
from post.models import Post
from .commons import add_login_context

class ModeratorView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    template_name = 'moderator.html'
    model = Post

    def post(self, request):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('home'))
        else:
            object_id = request.POST.get('id')
            if 'post-delete' in request.POST:
                post = get_object_or_404(Post, id=object_id)
                post.is_trashed = True
                post.save()
            elif 'post-recover' in request.POST:
                post = get_object_or_404(Post, id=object_id)
                post.is_trashed = False
                post.save()
            elif 'comment-delete' in request.POST:
                comment = get_object_or_404(Comment, id=object_id)
                comment.is_trashed = True
                comment.save()
            elif 'comment-recover' in request.POST:
                comment = et_object_or_404(Comment, id=object_id)
                comment.is_trashed = False
                comment.save()
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super(ModeratorView, self).get_context_data(**kwargs)
        context = add_login_context(context)
        context['form'] = ModeratorFilterForm()
        to_search_query = self.request.GET.get('to_search')
        if to_search_query == '1':
            context = self.add_comment_context(context)
        else:
            context = self.add_post_context(context)
        return context

    def test_func(self):
        """ Tests if the user is a superuser/moderator """
        
        if not self.request.user.is_superuser :
            raise PermissionDenied("You are not a moderator")
        return True

    ### helper functions

    def add_comment_context(self, context):
        """ Adds filtered comment instances to context"""

        comments = Comment.objects.all().order_by('-last_modified')
        filtered = self.apply_query_fields(comments, QueryType.Comment)
        context['is_comment'] = True
        context['is_post'] = False
        context['comments'] = filtered
        return context

    def add_post_context(self, context):
        """ Adds filtered post instances to context"""

        posts = Post.objects.all().order_by('-last_modified')
        filtered = self.apply_query_fields(posts, QueryType.Post)
        context['posts'] = filtered
        context['is_comment'] = False
        context['is_post'] = True
        return context

    def apply_query_fields(self, to_filter, query_type):
        """ Filters by the query fields specified in ModeratorForm """

        user_query = self.request.GET.get('user')
        date_from_query = self.request.GET.get('date_from')
        date_to_query = self.request.GET.get('date_to')
        is_deleted_query = self.request.GET.get('is_deleted')

        if user_query != '' and user_query is not None:
            to_filter = to_filter.filter(user__icontains=user_query)
        if date_from_query != '' and date_from_query is not None:
            to_filter = to_filter.filter(last_modified__date__gte=date_from_query)
        if date_to_query != '' and date_to_query is not None:
            to_filter = to_filter.filter(last_modified__date__lte=date_to_query)
        if is_deleted_query != '' and is_deleted_query is not None:
            to_filter = to_filter.filter(is_trashed=is_deleted_query)
        else:
            to_filter = to_filter.filter(is_trashed=False)

        title_query = self.request.GET.get('title')
        if title_query != '' and title_query is not None:
            if query_type == QueryType.Post:
                to_filter = to_filter.filter(title__icontains=title_query)
            else:
                to_filter = to_filter.filter(post__title__icontains=title_query)

        return to_filter

        

class QueryType(Enum):
    Post = 1
    Comment = 2