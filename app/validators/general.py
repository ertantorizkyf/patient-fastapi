import re


def is_sex_valid(sex):
    return True if sex.upper() == 'M' or sex.upper() == 'F' else False


def is_phone_valid(phone):
    return True if phone.isnumeric() else False


def is_email_valid(email):
    mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if re.fullmatch(mail_regex, email) else False
