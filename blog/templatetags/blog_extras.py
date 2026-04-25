from django import template
import math

register = template.Library()


@register.filter
def reading_time(text):
    if not text:
        return 1
    
    words = len(text.split())
    minutes = math.ceil(words/300)
    return minutes if minutes >= 1 else 1