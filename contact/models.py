from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class AddressType(models.Model):
	value = models.CharField(max_length=20)
	def __str__(self):
		return self.value.__str__()

class Address(models.Model):
	_type = models.ForeignKey(AddressType)
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	zip_code = models.CharField(max_length=15)
	country = models.CharField(max_length=40)

class PhoneNumber(models.Model):
	value = PhoneNumberField()

class Email(models.Model):
	value = models.EmailField()

class WebPage(models.Model):
	url = models.URLField()

class NameType(models.Model):
	value = models.CharField(max_length=20)
	def __str__(self):
		return self.value.__str__()

class Name(models.Model):
	_type = models.ForeignKey(NameType)
	value = models.CharField(max_length=30)

class Contact(models.Model):
	names = models.ManyToManyField(Name) 
	phoneNumbers = models.ManyToManyField(PhoneNumber)
	webPages = models.ManyToManyField(WebPage)
	emails = models.ManyToManyField(Email)
	addresss = models.ManyToManyField(Address)

