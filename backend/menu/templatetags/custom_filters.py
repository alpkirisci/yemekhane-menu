from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None

# @register.filter
# def get_model_name(obj):
#     try:
#         return obj.__name__
#     except AttributeError:
#         return None