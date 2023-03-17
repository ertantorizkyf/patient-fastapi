def phone_formatter(phone):
    if phone[0] == '0':
        phone = '62' + phone[1:]
    phone = phone.replace('+', '')
    phone = phone.replace(' ', '')
    phone = phone.replace('-', '')
    return phone
