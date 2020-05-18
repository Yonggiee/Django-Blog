from django.forms import ModelForm
from django import forms

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'desc',)

class FilterForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    user = forms.CharField(required=False)
    title = forms.CharField(required=False)

