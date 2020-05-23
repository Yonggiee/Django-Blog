from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class ModeratorFilterForm(forms.Form):
    """
    A form class that is used in ModeratorView for moderators to
    filter the information displayed in the table.
    Users can toggle between comments and posts
    """

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

    user = forms.CharField(required=False)
    title = forms.CharField(required=False)
    date_from = forms.DateField(required=False, widget=DateInput)
    date_to = forms.DateField(required=False, widget=DateInput)
    
