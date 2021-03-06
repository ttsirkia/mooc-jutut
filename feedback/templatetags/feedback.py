from django import template


register = template.Library()


@register.filter
def grade_color(grade):
    colors = ['danger', 'warning', 'success']
    if grade is not None:
        try:
            grade = int(grade)
            if 0 <= grade < len(colors):
                return colors[grade]
        except ValueError:
            pass
    return 'default'

@register.filter
def fill_format_string(fmt, value):
    parts = tuple(value.split(','))
    return fmt % parts


@register.filter
def force_int(string):
    try:
        return int(string)
    except ValueError:
        return None
