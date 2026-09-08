from django import template

register = template.Library()


@register.filter
def split_comma(value):
    """Split 'Friendly, Smart, Obedient' into ['Friendly', 'Smart', 'Obedient']."""
    if not value:
        return []
    return [part.strip() for part in value.split(',') if part.strip()]
