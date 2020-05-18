"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import HomeView, PostDetailedView, PostCreateView, PostUpdateView, UserCreateView, UserLoginView, ModeratorView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^new-post/$', PostCreateView.as_view(), name="post_new"),
    url(r'^new-user/$', UserCreateView.as_view(), name="user_new"),
    url(r'^moderator/$', ModeratorView.as_view(), name="moderator"),
    url(r'^login/', UserLoginView.as_view(), name="user_login"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailedView.as_view(), name="detailed"),
    url(r'^edit/(?P<slug>[\w-]+)/$', PostUpdateView.as_view(), name="post_edit"),
]
