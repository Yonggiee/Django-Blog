from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_one_alphanum(string):
    if not any(char.isalnum() for char in string):
        raise ValidationError(
            _('%(string)s does not have at least one alphanumeric'),
            params={'string': string},
        )
