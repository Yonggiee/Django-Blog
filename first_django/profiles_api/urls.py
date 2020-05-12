from django.conf.urls import url

from . import views

urlpatterns = [
    url('hello-view/', views.HelloApiView.as_view()),
]