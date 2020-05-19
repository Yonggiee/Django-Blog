from django import forms


class FilterForm(forms.Form):
    date_from_day = forms.IntegerField(required=False)
    date_from_month = forms.IntegerField(required=False)
    date_from_year = forms.IntegerField(required=False)
    date_to_day = forms.IntegerField(required=False)
    date_to_month = forms.IntegerField(required=False)
    date_to_year = forms.IntegerField(required=False)
    user = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'user-filter'}))
    title = forms.CharField(required=False)
