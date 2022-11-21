import json

from django import template

register = template.Library()

@register.filter
def graph_data_labels(value):

	value = json.loads(value)
	labels = value['labels']

	return labels

@register.filter
def graph_data_values(value):

	value = json.loads(value)
	data = value['data']

	return data

@register.filter
def graph_data_title(value):

	value = json.loads(value)
	data = value['title']

	return data