import re
from settings import APPLIED_KEYWORDS

def parse_mail(message):
    parsed_data = {
        'company_name': 'Not Specified',
        'role': 'Not Specified',
        'status': None,
        'experience_level': 'Not Specified',
        'job_id': 'Not Specified',
        'work_type': 'Not Specified',
        'location': 'Not Specified',
        'country': 'Not Specified'
    }

    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
    snippet = message.get('snippet', '').lower()

    is_applied_email = any(keyword in snippet for keyword in APPLIED_KEYWORDS)

    if  is_applied_email:
        parsed_data['status'] = 'Applied'
    else:
        return None

    parsed_data['company_name'] = 'placeholder_company'
    parsed_data['role'] = subject

    return parsed_data

