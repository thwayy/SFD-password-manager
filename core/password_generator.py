# functionality for password generator
import secrets # to generate cryptographically secure passwords
import string # to get characters

UPPERCASE = string.ascii_uppercase # A-Z
LOWERCASE = string.ascii_lowercase # a-z
NUMBERS = string.digits            # 0-9
SPECIAL = "!@#$%^&*()-_=+?"        # special characters

# to return the parameters selected in generator_view
def get_parameters(use_upper, use_lower, use_numbers, use_special):
    ticked = []
    if use_upper:
        ticked.append(UPPERCASE)
    if use_lower:
        ticked.append(LOWERCASE)
    if use_numbers:
        ticked.append(NUMBERS)
    if use_special:
        ticked.append(SPECIAL)
    return ticked

def generate_password(length, use_upper, use_lower, use_numbers, use_special):
    # get the selected parameters
    parameters = get_parameters(use_upper, use_lower, use_numbers, use_special)
    # must select at least one parameter
    if not parameters:
        raise ValueError("Pick at least one character type.")

    password = []

    # select one character from each parameter type
    for p in parameters:
        password.append(secrets.choice(p))
    # after parameters are met, fill up the length with any character from select parameters
    available_chars = "".join(parameters)
    while len(password)<length:
        password.append(secrets.choice(available_chars))
    # shuffle order of the characters selected using SystemRandom to be cryptographically secure
    secrets.SystemRandom().shuffle(password)
    return "".join(password) 

    