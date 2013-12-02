from django import template

register = template.Library()

@register.filter(name='addcssclass')
def addcss(field, css):
	return field.as_widget(attrs={"class":css})

@register.filter('klass')
def klass(ob):
	return ob.__class__.__name__
