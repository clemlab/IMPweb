from django.apps import AppConfig
from django.core.signals import request_finished
from django.contrib.auth.signals import user_logged_in as django_login
from allauth.account.signals import user_signed_up, user_logged_in, email_confirmed
from .uni_app import load_data

from .signals import murder_console


# Mainly used for implementing signals stuff for testing purposes. 
class ProjectConfig(AppConfig):
	name = 'memprot_project'

	def ready(self):
		# MAKE SURE THIS IS CALLED AT SERVER START
		# HENCE THE PRINT STATEMENT VV DOWN HERE VV
		for i in range(10): 
			print('memprot_signals linked in')
		user_signed_up.connect(murder_console)
		email_confirmed.connect(murder_console)
		load_data()