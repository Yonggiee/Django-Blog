from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import ArticleList, ArticleDetail, CommentList

urlpatterns = [
    url(r'^articles/$', ArticleList.as_view(), name='article-list'),
    url(r'^articles/(?P<pk>[0-9]+)/$',
        ArticleDetail.as_view(), name='article-details'),
    url(r'^articles/(?P<pk>[0-9]+)/comments/$',
        CommentList.as_view(), name='article-comments'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
