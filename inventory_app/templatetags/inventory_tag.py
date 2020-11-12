from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def process_edit(process, pk):
	path = 'inventory:'+process+'_update'
	url_path = reverse(path,kwargs={'pk': pk})
	link = "<a href='%s'>Edit</a>"%url_path
	return mark_safe(link)


