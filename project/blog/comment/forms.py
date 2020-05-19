from django.forms import ModelForm

from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['style']='resize:none;'
        self.fields['body'].widget.attrs['rows']=5

# {% for field in form %}
#         {{ field }}
#         {% for error in field.errors %}
#             <p>{{error}}</p>
#         {% endfor %}
#         {% endfor %}