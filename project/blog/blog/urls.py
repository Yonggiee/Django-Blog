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

from .views import post_edit, HomeView, PostDetailedView, PostCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^new/$', PostCreateView.as_view(), name="post_new"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailedView.as_view(), name="detailed"),
    url(r'^edit/(?P<slug>[\w-]+)/$', post_edit, name="post_edit")
]