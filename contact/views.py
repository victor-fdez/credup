from django.shortcuts import render
from contact.forms import AddressForm, ContactForm

# Create your views here.

def contact_add(request):
	if request.method == 'GET':
		contactForm = ContactForm()
		return render(request, 'contact/contact.html', dictionary={'ContactForm': contactForm})
	else:
		contactForm = ContactForm(request=request)
		if contactForm.is_valid():
			#create new contact and redirect to contact form contact/11334533/
			print 'success form was valid'
		return render(request, 'contact/contact.html', dictionary={'ContactForm': contactForm})
			

def contact_edit(request):
	pass

def contact_view(request):
	pass

