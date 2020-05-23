from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'desc', 'user', 'date_created',
            'last_modified', 'is_trashed', 'slug')

