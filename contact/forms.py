import sys
import inspect
from django import forms
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext, ugettext_lazy as _ 
from contact.models import Address, PhoneNumber, Email, WebPage, Name, Contact


class AddressForm(forms.ModelForm):
	formsetTitle = 'Addresses'	
	class Meta:
		model = Address
		fields = ('_type', 'street', 'city', 'state', 'zip_code', 'country', )

class PhoneNumberForm(forms.ModelForm):
	formsetTitle = 'Phone Numbers'	
	class Meta:
		model = PhoneNumber
		fields = ('value', )
		labels = {
			'value': _('phone'),
		}

class EmailForm(forms.ModelForm):
	formsetTitle = 'Emails'	
	formsetInitial = [{'value': 'email',},]
	formsetMinimum = 1
	class Meta:
		model = Email
		fields = ('value', )
		labels = {
			'value': _('email'),
		}

class WebPageForm(forms.ModelForm):
	formsetTitle = 'Pages'	
	class Meta:
		model = WebPage
		fields = ('url', )
	
class NameFormSet(BaseFormSet):
		
	def clean(self):
		if any(self.errors):
			return
		errors = []
		firstNameForm = self.getNameTypeForm(1)
		lastNameForm = self.getNameTypeForm(3)
		if firstNameForm is None:
			errors.append(forms.ValidationError(_('A first name must be entered')))
		if lastNameForm is None:
			errors.append(forms.ValidationError(_('A last name must be entered')))
		if any(errors):
			raise forms.ValidationError(errors)
		
	def getNameTypeForm(self, _type):
		for form in self.forms:
			if form.cleaned_data['_type'] == _type:
				return form
		return None
	
class NameForm(forms.ModelForm):
	formsetTitle = 'Names'	
	formsetInitial = [{'_type': 1, 'value': '',}, {'_type': 3, 'value': '',},]
	formsetMinimum = 2
	formsetClass = NameFormSet
	class Meta:
		model = Name
		fields = ('_type', 'value', )
		labels = {
			'value': _('name'),
		}

class ContactForm:
	"""
	ContactForm

	This for is made up of formsets each of a different form class. The
	from classes are all contained within this python file.
	"""
	#get all class objects within this file
	FormClassObjects = filter(lambda c: c[1].__name__[-4:] == "Form" and c[1].__module__ == "contact.forms", inspect.getmembers(sys.modules[__name__], inspect.isclass))
	def __init__(self, contactId = None):
		"""
		contactId - numeric representation of contact id
		"""
		contact = None
		if contactId is not None:
			contact = Contact.get(id=contactId)
		#get formsets for every possible form
		self.formsets = {}
		for s, formClass in self.FormClassObjects:
			initial = []
			if contact is None:
				initial = getattr(formClass, 'formsetInitial', None)
			classFormSet = self.getFormSet(formClass, contact=contact, initial=initial)	
			classFormSet.formsetTitle = formClass.formsetTitle
			self.formsets[formClass.__name__[0].lower() + formClass.__name__[1:] + 'Set'] = classFormSet
		
	def getFormSet(self, formClass, contact = None, initial = []):
		formset = None
		modelName = formClass.__name__[:-4]
		formsetFactory = formset_factory(
						formClass, 
						formset=getattr(formClass, 'formsetClass', BaseFormSet),
						extra=0, 
						can_delete=True, 
						max_num=10
						)
		if contact is not None:
			#get all objects references by the Contact and create
			#a formset with the given objects
			contactAttrName = modelName[1].lower() + modelName[1:] + 's'
			formsetObjects = getattr(contact, contactAttrName).all()
		formset = formsetFactory(prefix=modelName, initial=initial)
		return formset

"""
class ContactForm(forms.ModelForm):

	title = 'Contact'
	title_submit = 'save'
	
	class Meta:
		model = Contact
		fields = ("names", "phones", "pages", "emails", "addresses",)
"""

