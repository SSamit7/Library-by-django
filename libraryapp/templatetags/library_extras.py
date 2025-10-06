from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_days(date, days):
    """Add days to a date"""
    return date + timedelta(days=days)

@register.filter
def multiply(value, arg):
    """Multiply the arg and value"""
    return int(value) * int(arg)