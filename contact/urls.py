from django.conf.urls import patterns, include, url

urlpatterns = patterns('contact.views',
	url(r'^add/$', 'contact_add'),
)
