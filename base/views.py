from django.shortcuts import render
from django.template.loader import get_template
from django.template.context import Context
from django.http.response import HttpResponse


# Create your views here.
def main(request):
	print request.user
	return render(request, '__base_site_template.html')

def login(request):
	return render(request, '__base_site_template.html')
