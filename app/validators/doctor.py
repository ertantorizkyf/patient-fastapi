from app.validators import general as GeneralValidator


def validate_time_slot_payload(time_slot):
    is_day_valid = GeneralValidator.is_day_name_valid(time_slot.day)
    if not is_day_valid:
        response = {
            'message': 'Day name not valid. Accepted day names are [Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]',
            'data': None
        }
        return response
    is_start_time_valid = GeneralValidator.is_time_valid(time_slot.start_time)
    if not is_start_time_valid:
        response = {
            'message': 'Start time not valid. Accepted time format is hh:mm (eg. 18:00)',
            'data': None
        }
        return response
    is_end_time_valid = GeneralValidator.is_time_valid(time_slot.end_time)
    if not is_end_time_valid:
        response = {
            'message': 'End time not valid. Accepted time format is hh:mm (eg. 18:00)',
            'data': None
        }
        return response
    return None
