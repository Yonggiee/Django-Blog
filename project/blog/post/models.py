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

    __original_title = None
    __original_desc = None


    ####### kkm

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        title_is_changed = self.title == self.__original_title
        desc_is_changed = self.desc == self.__original_desc
        if self.title != self.__original_title:
            super(Post, self).save(force_insert, force_update, *args, **kwargs)
            self.__original_title = self.title
            self.__original_desc = self.desc

    def changed(self, changed_post):
        title_is_changed = self.title == changed_post.title
        desc_is_changed = self.desc == changed_post.title

        return title_is_changed or desc_is_changed