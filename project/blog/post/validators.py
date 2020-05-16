from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_symbol(string):
    special = 0
    for i in range(len(string)):
        if(string[i].isalpha()):
            continue
        elif(string[i].isdigit()):
            continue
        else:
            special = special + 1
    if special > 50:
        raise ValidationError(
            _('%(string)s have more than 50 symbols'),
            params={'string': string},
        )
        