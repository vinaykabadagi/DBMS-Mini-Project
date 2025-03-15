from django import template
from datetime import timedelta
from django.db.models import Sum

register = template.Library()

@register.filter
def sum_quantity(batches):
    """Calculate total quantity from a queryset of batches"""
    if not batches:
        return 0
    try:
        # Try using aggregate for efficiency if it's a queryset
        if hasattr(batches, 'aggregate'):
            return batches.aggregate(total=Sum('quantity'))['total'] or 0
        # Fall back to Python sum for regular iterables
        return sum(batch.quantity for batch in batches)
    except (AttributeError, TypeError):
        return 0

@register.filter
def timedelta_days(value, arg):
    """Add/subtract days from a date"""
    try:
        return value + timedelta(days=int(arg))
    except (ValueError, TypeError):
        return value 