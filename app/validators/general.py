import datetime
import re
import time


def is_sex_valid(sex):
    return True if sex.upper() == 'M' or sex.upper() == 'F' else False


def is_phone_valid(phone):
    return True if phone.isnumeric() else False


def is_email_valid(email):
    mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return True if re.fullmatch(mail_regex, email) else False


def is_iso_format_date_valid(date):
    try:
        datetime.date.fromisoformat(date)
        return True
    except ValueError:
        return False


def is_day_name_valid(day):
    days = [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
    ]
    return True if day in days else False


def is_time_valid(time_str):
    try:
        time.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False
