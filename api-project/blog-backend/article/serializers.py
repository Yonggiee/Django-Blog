from rest_framework import serializers

from comment.serializers import CommentSerializer
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'desc', 'user', 'date_created',
            'last_modified', 'is_trashed', 'slug')

class ArticleCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ('comments',)
