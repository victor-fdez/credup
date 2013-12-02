from django.shortcuts import render
from contact.forms import AddressForm, ContactForm

# Create your views here.

def contact_add(request):
	if request.method == 'GET':
		return render(request, 'contact/contact.html', dictionary={'ContactForm': ContactForm()})
	else:
		return render(request, 'contact/contact.html', dictionary={'ContactForm': ContactForm()})
			

def contact_edit(request):
	pass

def contact_view(request):
	pass

