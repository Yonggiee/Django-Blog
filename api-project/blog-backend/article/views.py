from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from .models import Article
from .serializers import ArticleSerializer, ArticleCommentSerializer
from comment.serializers import CommentSerializer


class ArticleList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Article.objects.all().order_by('-last_modified')
    serializer_class = ArticleSerializer
    
    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return (AllowAny(),)
    #     return (IsAuthenticated(),)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def put(self, request, *args, **kwargs):
        articles_list = request.data
        for article in articles_list:
            pk = article['id']
            title = article['title']
            desc = article['desc']
            article_to_change = Article.objects.get(pk=pk)
            article_to_change.title = title
            article_to_change.desc = desc
            article_to_change.save()
        return self.get(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"user": self.request.user.id}

class ArticleDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Article.objects.all()        ### why is queryset all when it is one object?
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return (AllowAny(),)
    #     return (IsAuthenticated(),)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentList(generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCommentSerializer
    lookup_field = 'slug'
    #permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        comments = CommentSerializer(self.get_object().comments, many=True)
        comments_json = comments.data
        return Response(comments_json)

