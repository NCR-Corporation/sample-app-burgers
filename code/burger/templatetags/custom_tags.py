from django import template
import random


register = template.Library()



@register.simple_tag
def randomNumberGenerator():
    numbers = [1,2,3]
    return random.choice(numbers)



