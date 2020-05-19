from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.contrib.auth.forms import AuthenticationForm

from comment.forms import CommentForm
from comment.models import Comment
from post.forms import PostForm, FilterForm, ModeratorFilterForm
from post.models import Post
from user.forms import SignUpForm
    

