from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.context import Context
from django.http.response import HttpResponse
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from base.forms import AdvUserCreationForm
from base.models import UserSignUpVerifier

gvd = { 'home_url': '/home/',
	'profile_url': '/profile/',
	'login_url': '/accounts/login/',
	'logout_url': '/accounts/logout/',
	'reset_url': '/accounts/reset/',
	'register_url': '/accounts/register/'}


def gvd_with(dictionary=dict()):
	return dict(gvd.items() + dictionary.items())

def render_msg(request, start='', middle='', end=''):
	return render(request, '__small_center_content_msg.html',
		dictionary=gvd_with({'msg': { 'start': start,
				              'middle': middle,
				              'end': end }}))


# Create your views here.
def main(request):
	return render(request, '__base_site_template.html', dictionary=gvd)

def login_view(request):
	if request.user.is_authenticated():
		return redirect('/home/')
	else:
		return login(request, 'registration/login.html', extra_context=gvd)

def logout_view(request):
	return logout(request, '/home/', extra_context=gvd)

def reset_view(request):
	return redirect('/')

@csrf_protect
@transaction.atomic
def register_view(request):
	if request.method == "GET":
		f = AdvUserCreationForm()
		print gvd_with({'form': f})
		return render(request, 'registration/register.html', dictionary=gvd_with({'form': f}))
	else:
		f = AdvUserCreationForm(request.POST)
		if f.is_valid():
			data = f.cleaned_data
			print 'password=', data['password1']
			user = User.objects.create_user(data['username'],
							data['email'],
							data['password1'])
			user.first_name = data['first_name']
			user.last_name = data['last_name']
			user.is_active = False
			verifier = UserSignUpVerifier(user=user)	
			user.save()
			verifier.save()
			send_mail('email verification',
				'please follow these link so that your email may be verified\n'
				'\n'
				'\thttp://www.credup.com%s' % verifier.get_absolute_url(),
				'victor.j.fdez@gmail.com',
				[user.email])
			return render_msg(request, 'An email will be sent to ', verifier.email, ' for verification')
		return render(request, 'registration/register.html', dictionary=gvd_with({'form': f}))

@transaction.atomic
def signup_verifier_view(request, key):
	"""
	First check that key is legitimate, if so the user for that
	key is activated
	"""
	verifier = None
	print 'get key is %s' % key
	try:
		verifier = UserSignUpVerifier.objects.get(code=key)
	except ObjectDoesNotExist:
		return redirect('/')
	user = User.objects.get(email=verifier.email)	
	user.is_active = True
	user.save()
	verifier.delete()
	return render_msg(request, 'Thank you, account %s has been verified' % user.username)

