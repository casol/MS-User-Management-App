import datetime
from django import template

register = template.Library()


@register.filter(name='calculate_age')
def calculate_age(birth_date):
    """Calculate user age and return permission."""
    today = datetime.date.today()
    try:
        age = (today.year
               - birth_date.year
               - ((today.month, today.day)
               < (birth_date.month, birth_date.day)))
    except AttributeError:
        return ''
    else:
        if age > 13:
            return 'Allowed'
        else:
            return 'Blocked'
