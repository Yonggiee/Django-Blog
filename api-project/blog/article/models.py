from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, RegexValidator
from django.conf import settings
from django.db import models
from django.urls import reverse

from .validators import validate_symbol

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200, unique=True,
        validators=[validate_symbol]
    )
    desc = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='title', always_update=True, unique=True, null=True)
     ## number of comments validate during insertion instead

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'slug': self.slug})
