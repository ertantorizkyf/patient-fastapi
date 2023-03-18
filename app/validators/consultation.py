from app.validators import general as GeneralValidator


def validate_consulation_date(consultation, time_slot):
    if not GeneralValidator.is_iso_format_date_valid(consultation.date):
        response = {
            'message': 'Please enter valid date. Valid format is year-month-date (eg. 2000-12-01)',
            'data': None
        }
        return response
    if GeneralValidator.is_date_lte_today(consultation.date):
        response = {
            'message': 'Only consultation where today is at least 1 day prior to consultation date can be created',
            'data': None
        }
        return response
    if not GeneralValidator.does_date_match_day_name(consultation.date, time_slot.day):
        response = {
            'message': 'Date does not match time slot day',
            'data': None
        }
        return response
    return None
