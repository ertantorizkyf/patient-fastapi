from app.validators import general as GeneralValidator

def validate_payload(patient): 
    if not GeneralValidator.is_sex_valid(patient.sex):
        response = {
            'message': 'Please enter valid sex (M/F)',
            'data': None
        }
        return response
    if not GeneralValidator.is_phone_valid(patient.phone):
        response = {
            'message': 'Please enter valid phone number',
            'data': None
        }
        return response
    if not GeneralValidator.is_phone_valid(patient.emergency_contact_phone):
        response = {
            'message': 'Please enter valid phone number',
            'data': None
        }
        return response
    if not GeneralValidator.is_email_valid(patient.email):
        response = {
            'message': 'Please enter valid email',
            'data': None
        }
        return response
    if not GeneralValidator.is_iso_format_date_valid(patient.dob):
        response = {
            'message': 'Please enter valid date of birth. Valid format is year-month-date (eg. 2000-12-01)',
            'data': None
        }
        return response
    return None