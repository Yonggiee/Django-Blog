from django.forms import ModelForm

from comment.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['style']='resize:none;'
        self.fields['body'].widget.attrs['rows']=5
