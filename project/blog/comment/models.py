from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from .validators import validate_one_alphanum

# Create your models here.
class Comment(models.Model):
    user = models.CharField(max_length=255)
    body = models.TextField(validators=[MinLengthValidator(32), validate_one_alphanum])
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE,)
    last_modified = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField(default=False)
