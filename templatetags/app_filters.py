from django import template

register = template.Library()

@register.filter(name='image_large')
def image_large(value):
	return value