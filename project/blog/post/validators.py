from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_symbol(string):
    """
    Raises a ValidationError if the string contains more than 50 symbols
    """

    special_chars = 0
    for i in range(len(string)):
        if(string[i].isalpha()):
            continue
        elif(string[i].isdigit()):
            continue
        else:
            special_chars = special_chars + 1
    if special_chars > 50:
        raise ValidationError(
            _('%(string)s have more than 50 symbols'),
            params={'string': string},
        )
        