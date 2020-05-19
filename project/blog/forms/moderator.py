from django import forms

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
    

