from django import template

register = template.Library()

@register.filter
def add_prefix(value, arg):
    """add some prefix for the given string"""
    return arg + str(value)

@register.filter
def get_range(value):
    '''return a list [0,value-1]'''
    return range(value)

@register.filter
def keyvalue(dict, key):
    ''' return dict keyvalue'''
    return dict[key]
