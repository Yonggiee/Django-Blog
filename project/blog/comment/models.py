from django.db import models

# Create your models here.
class Comment(models.Model):
    user = models.CharField(max_length=255)
    body = models.TextField()
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE,)
    last_modified = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField()