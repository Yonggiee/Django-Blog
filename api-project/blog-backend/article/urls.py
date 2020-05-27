from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import ArticleList, ArticleDetail, CommentList

urlpatterns = [
    url(r'^articles/$', ArticleList.as_view(), name='article-list'),
    url(r'^article/(?P<slug>[\w-]+)/$',
        ArticleDetail.as_view(), name='article-details'),
    url(r'^article/(?P<slug>[\w-]+)/comments/$',
        CommentList.as_view(), name='article-comments'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
