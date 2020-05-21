from django import forms

class FilterForm(forms.Form):
    """
    A form class that is used in HomeView for users to
    filter the post displayed in the table
    """

    date_from_day = forms.IntegerField(required=False, min_value=0, max_value=31)
    date_from_month = forms.IntegerField(required=False, min_value=0, max_value=12)
    date_from_year = forms.IntegerField(required=False, min_value=0)
    date_to_day = forms.IntegerField(required=False, min_value=0, max_value=31)
    date_to_month = forms.IntegerField(required=False, min_value=0, max_value=12)
    date_to_year = forms.IntegerField(required=False, min_value=0)
    user = forms.CharField(required=False)
    title = forms.CharField(required=False)
