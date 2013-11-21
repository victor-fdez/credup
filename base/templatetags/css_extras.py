from django import template

register = template.Library()

@register.filter(name='addcssclass')
def addcss(field, css):
	   return field.as_widget(attrs={"class":css})
