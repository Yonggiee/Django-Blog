from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from comment.models import Comment
from forms.moderator import ModeratorFilterForm
from post.models import Post
from .commons import add_login_context

class ModeratorView(LoginRequiredMixin, ListView):
    template_name = 'moderator.html'
    model = Post

    def post(self, request):
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect(reverse('home'))
        elif 'post-delete' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            post.is_trashed = True
            post.save()
        elif 'post-recover' in request.POST:
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            post.is_trashed = False
            post.save()
        elif 'comment-delete' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            comment.is_trashed = True
            comment.save()
        elif 'comment-recover' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            comment.is_trashed = False
            comment.save()
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super(ModeratorView, self).get_context_data(**kwargs)
        context = add_login_context(context)
        context['form'] = ModeratorFilterForm()

        title_query = self.request.GET.get('title')
        user_query = self.request.GET.get('user')
        date_from_query = self.request.GET.get('date_from')
        date_to_query = self.request.GET.get('date_to')
        is_deleted_query = self.request.GET.get('is_deleted')
    
        to_search_query = self.request.GET.get('to_search')

        if to_search_query == '1':
            comments = Comment.objects.using('PostsAndComments').all().order_by('-last_modified')

            if title_query != '' and title_query is not None:
                comments = comments.filter(post__title__icontains=title_query)
            if user_query != '' and user_query is not None:
                comments = comments.filter(user__icontains=user_query)
            if date_from_query != '' and date_from_query is not None:
                posts = posts.filter(last_modified__date__gte=date_from_query)
            if date_to_query != '' and date_to_query is not None:
                posts = posts.filter(last_modified__date__lte=date_to_query)
            if is_deleted_query != '' and is_deleted_query is not None:
                comments = comments.filter(is_trashed=is_deleted_query)
            else:
                comments = comments.filter(is_trashed=False)

            context['comments'] = comments
            context['is_comment'] = True
            context['is_post'] = False

        else:
            posts = Post.objects.using('PostsAndComments').all().order_by('-last_modified')

            if title_query != '' and title_query is not None:
                posts = posts.filter(title__icontains=title_query)
            if user_query != '' and user_query is not None:
                posts = posts.filter(user__icontains=user_query)
            if date_from_query != '' and date_from_query is not None:
                posts = posts.filter(last_modified__date__gte=date_from_query)
            if date_to_query != '' and date_to_query is not None:
                posts = posts.filter(last_modified__date__lte=date_to_query)
            if is_deleted_query != '' and is_deleted_query is not None:
                posts = posts.filter(is_trashed=is_deleted_query)
            else:
                posts = posts.filter(is_trashed=False)

            context['posts'] = posts
            context['is_comment'] = False
            context['is_post'] = True

        return context