import re
from django.core.exceptions import ValidationError

def validate_username_one_or_two_names(value):
    # Trim leading/trailing spaces
    value = value.strip()

    # Ensure the username is not empty
    if not value:
        raise ValidationError("Username cannot be empty.")

    # Regular expression to allow one or two alphabetic words (letters and a space in between)
    regex = r'^[a-zA-Z]+(?: [a-zA-Z]+)?$'  # Allows one or two alphabetic words, separated by a space

    # Check if the value matches the regex pattern
    if not re.match(regex, value):
        raise ValidationError("Username must consist of one or two alphabetic words separated by a space.")

    return value





