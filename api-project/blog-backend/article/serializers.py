from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from comment.serializers import CommentSerializer
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    last_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
      return obj.user.username

    class Meta:
        model = Article
        fields = ('id', 'title', 'desc', 'user', 'date_created',
            'last_modified', 'is_trashed', 'slug')
        extra_kwargs = {
            'user': {'required': False}
        }

class ArticleCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ('comments',)
