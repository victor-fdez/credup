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
	formsetOrder = 3
	class Meta:
		model = Address
		fields = ('_type', 'street', 'city', 'state', 'zip_code', 'country', )

class PhoneNumberForm(forms.ModelForm):
	formsetTitle = 'Phone Numbers'	
	formsetOrder = 4
	class Meta:
		model = PhoneNumber
		fields = ('value', )
		labels = {
			'value': _('phone'),
		}

class EmailFormSet(BaseFormSet):
		
	def clean(self):
		if len(self.forms) <= 0:
			raise forms.ValidationError(_(u'Atleast one email must be provided'))


class EmailForm(forms.ModelForm):
	formsetTitle = 'Emails'	
	formsetInitial = [{'value': 'email',},]
	formsetMinimum = 1
	formsetOrder = 2
	formsetClass = EmailFormSet
	class Meta:
		model = Email
		fields = ('value', )
		labels = {
			'value': _('email'),
		}

class WebPageForm(forms.ModelForm):
	formsetTitle = 'Pages'	
	formsetOrder = 5
	class Meta:
		model = WebPage
		fields = ('url', )
	
class NameFormSet(BaseFormSet):
		
	def clean(self):
		errors = []
		firstNameForm = self.getNameTypeForm(1)
		lastNameForm = self.getNameTypeForm(3)
		if firstNameForm is None:
			errors.append(forms.ValidationError(_('A first name must be entered')))
		if lastNameForm is None:
			errors.append(forms.ValidationError(_('A last name must be entered')))
		print errors
		if any(errors):
			raise forms.ValidationError(errors)
		
	def getNameTypeForm(self, _type):
		for form in self.forms:
			if form.cleaned_data['_type'].id == _type:
				return form
		return None
	
class NameForm(forms.ModelForm):
	formsetTitle = 'Names'	
	formsetInitial = [{'_type': 1, 'value': '',}, {'_type': 3, 'value': '',},]
	formsetMinimum = 2
	formsetOrder = 1
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
	#get all class objects within this file, and sort them based on formsetOrder attribute of each class
	#this should be a number from 1 onwards
	FormClassObjects = sorted(
			filter(
				lambda c: c[1].__name__[-4:] == "Form" and c[1].__module__ == "contact.forms", inspect.getmembers(sys.modules[__name__], inspect.isclass)
				), key=lambda c: c[1].formsetOrder if c[1].formsetOrder else 10
				)
	def __init__(self, contactId = None, request = None):
		"""
		contactId - numeric representation of contact id
		"""
		contact = None
		if contactId is not None:
			contact = Contact.get(id=contactId)
		#get formsets for every possible form
		self.formsets = []
		for s, formClass in self.FormClassObjects:
			initial = []
			if contact is None:
				initial = getattr(formClass, 'formsetInitial', None)
			classFormSet = self.getFormSet(formClass, contact=contact, initial=initial, request=request)	
			classFormSet.formsetTitle = formClass.formsetTitle
			#self.formsets[formClass.__name__[0].lower() + formClass.__name__[1:] + 'Set'] = classFormSet
			self.formsets.append(classFormSet)
		
	def getFormSet(self, formClass, contact = None, initial = [], request = None):
		"""
		getFormSet

		there are 4 cases:

			1. No contact still, but need an empty form for the user
			to fill up. (GET)

			2. No contact still, but need to validate the input data
			so the request objects needs to be passed to each and every
			fomr set. (POST)

			3. Contact, and need to get contact specifc information and
			display it in form. (GET)

			4. Contact, need to pass in to every formset the request object
			so that contact information is validated. (POST)

		"""
		formset = None
		modelName = formClass.__name__[:-4]
		formsetFactory = formset_factory(
						formClass, 
						formset=getattr(formClass, 'formsetClass', BaseFormSet),
						extra=0, 
						can_delete=True, 
						max_num=10
						)
		if contact is None:
			if request is None:
				#case 1
				formset = formsetFactory(prefix=modelName, initial=initial)
			else:
				#case 2
				formset = formsetFactory(request.POST, request.FILES, prefix=modelName)
		else:
			if request is None:
				#case 3
				#get all objects references by the Contact and create
				#a formset with the given objects
				contactAttrName = modelName[1].lower() + modelName[1:] + 's'
				formsetObjects = getattr(contact, contactAttrName).all()
				formset = None
			else:
				#case 4
				formset = formsetFactory(request.POST, request.FILES, prefix=modelName)
		return formset

	def is_valid(self):
		"""
		Returns that it is valid only if all off the formsets are valid.
		"""
		return all(map(lambda form: form[1].is_valid(), self.formsets.items()))
