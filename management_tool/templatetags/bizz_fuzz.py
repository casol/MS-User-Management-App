from django import template

register = template.Library()


@register.filter(name='get_bizz_fuzz')
def get_bizz_fuzz(random_number):
    """Get BizzFuzz representation of a user random number."""
    try:
        if random_number % 3 == 0 and random_number % 5 == 0:
            return 'BizzFuzz'
        elif random_number % 3 == 0:
            return 'Bizz'
        elif random_number % 5 == 0:
            return 'Fuzz'
        else:
            return random_number
    except TypeError:
        return ''
