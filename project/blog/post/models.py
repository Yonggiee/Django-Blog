from autoslug import AutoSlugField
from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator
from django.urls import reverse

from .validators import validate_symbol

# Create your models here.
class Post(models.Model):
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=200, unique=True,
        validators=[validate_symbol]
    )
    desc = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='title', always_update=True, unique=True, null=True)
    number_of_comments = models.IntegerField(default=0, validators=[MaxValueValidator(50)])

    def get_absolute_url(self):
        return reverse('detailed', kwargs={'slug': self.slug})
