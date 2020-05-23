from django.core.validators import MinLengthValidator, RegexValidator
from django.conf import settings
from django.db import models
from .validators import validate_one_alphanum

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    body = models.TextField(validators=[MinLengthValidator(32), validate_one_alphanum])
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE,)
    last_modified = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField(default=False)
