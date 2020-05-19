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

class FilterForm(forms.Form):
    date_from_day = forms.IntegerField(required=False)
    date_from_month = forms.IntegerField(required=False)
    date_from_year = forms.IntegerField(required=False)
    date_to_day = forms.IntegerField(required=False)
    date_to_month = forms.IntegerField(required=False)
    date_to_year = forms.IntegerField(required=False)
    user = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'user-filter'}))
    title = forms.CharField(required=False)

class ModeratorFilterForm(forms.Form):
    SEARCH_OPTIONS = [
        ("0", "Posts"),
        ("1", "Comments"),
    ]

    DELETE_OPTIONS = [
        ("0", "No"),
        ("1", "Yes"),
    ]

    to_search = forms.MultipleChoiceField(
        choices=SEARCH_OPTIONS,
        initial='0',
        widget=forms.RadioSelect(),
        required=True,
        label='to_search',
    )

    is_deleted = forms.MultipleChoiceField(
        choices=DELETE_OPTIONS,
        initial='0',
        widget=forms.RadioSelect(),
        required=True,
        label='is_deleted',
    )

    date_from_day = forms.IntegerField(required=False)
    date_from_month = forms.IntegerField(required=False)
    date_from_year = forms.IntegerField(required=False)
    date_to_day = forms.IntegerField(required=False)
    date_to_month = forms.IntegerField(required=False)
    date_to_year = forms.IntegerField(required=False)
    user = forms.CharField(required=False)
    title = forms.CharField(required=False)
    

