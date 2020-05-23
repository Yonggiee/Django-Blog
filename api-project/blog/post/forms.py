from django.forms import ModelForm
from django import forms

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'desc',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['size']=102
        self.fields['desc'].widget.attrs['cols']=100
        self.fields['desc'].widget.attrs['style']='resize:none;'
        self.fields['desc'].widget.attrs['rows']=35

class MultipleUploadForm(forms.Form):
    """ A form class for users to upload multiple posts at once """

    file = forms.FileField()