import string
from random import choice	
from string import letters, digits
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_init

class UserSignUpVerifier(models.Model):
	"""
	Model is used to verify a users email after he or she
	has signed up.
	"""
	code = models.CharField(primary_key=True, db_index=True, max_length=64)
	email = models.EmailField()
	user = None
	def __init__(self, *args, **kwargs):
		    self.user = kwargs.pop('user', None)
		    super(UserSignUpVerifier, self).__init__(*args, **kwargs)
	
	def get_absolute_url(self):
		return "/registration/signup-verify/%s/" % self.code

def UserSignUpVerifierInit(**kwargs):
	"""
	generate verifier key
	"""
	instance = kwargs['instance']
	if instance.user:
		user = instance.user
		unique_found = False
		while not unique_found:
			rand_key = ''.join(choice(letters+digits) for i in range(64))
			try:
				UserSignUpVerifier.objects.get(code=rand_key)
			except ObjectDoesNotExist:
				unique_found = True
		instance.email = user.email
		instance.code = rand_key
		print 'Verifier key', rand_key, 'email is', user.email

post_init.connect(UserSignUpVerifierInit, UserSignUpVerifier)

