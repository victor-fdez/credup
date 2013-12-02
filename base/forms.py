from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _ 

class AdvUserCreationForm(UserCreationForm):
	"""
	AdvUserCreationForm allows for first name, and last name input. In
	the future it will allow a future user to request administrator
	priviledges, which will be granted after another administrator has
	allowed it
	"""
	title = 'Register'
	title_submit = 'Sign up'

	class Meta(UserCreationForm.Meta):
		fields = ('first_name', 'last_name', 'email',)
			
	def __init__(self, *args, **kwargs):
		super(AdvUserCreationForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True
	
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			user = User.objects.get(email=email)
		except ObjectDoesNotExist:
			return email
		raise forms.ValidationError(
			_('A user with that email already exists'),
			code='duplicate_email',
		)

	
