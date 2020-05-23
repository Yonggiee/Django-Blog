from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class FilterForm(forms.Form):
    """
    A form class that is used in HomeView for users to
    filter the post displayed in the table
    """

    date_from = forms.DateField(required=False, widget=DateInput)
    date_to = forms.DateField(required=False, widget=DateInput)
    user = forms.CharField(required=False)
    title = forms.CharField(required=False)
