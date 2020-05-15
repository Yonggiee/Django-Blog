from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=200, unique=True)
    desc = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField()