from django.contrib import admin
from base.models import UserSignUpVerifier

# Register your models here.
class UserSignUpVerifierAdmin(admin.ModelAdmin):
	pass


admin.site.register(UserSignUpVerifier, UserSignUpVerifierAdmin)
