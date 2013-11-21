from django.conf.urls import include, patterns, url

urlpatterns = patterns('base.views',
		url(r'^login/$', 'login_view'),
		url(r'^logout/$', 'logout_view'),
		url(r'^reset/$', 'reset_view'),
		url(r'^register/$', 'register_view'),
		url(r'^signup-verify/(?P<key>[0-9a-zA-Z]{64})/$', 'signup_verifier_view'),
)
