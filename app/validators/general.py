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


def is_date_lte_today(date):
    try:
        is_lte_today = datetime.date.fromisoformat(
            date).isoformat() <= datetime.datetime.now().isoformat()
        return True if is_lte_today else False
    except ValueError:
        return False


def does_date_match_day_name(date, ref_day):
    try:
        formatted_day = datetime.date.fromisoformat(date).strftime('%A')
        return True if formatted_day == ref_day else False
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
