from django.apps import AppConfig
from django.core.signals import request_finished
from django.contrib.auth.signals import user_logged_in as django_login
from allauth.account.signals import user_signed_up, user_logged_in, email_confirmed


from .signals import murder_console

class ProjectConfig(AppConfig):
	name = 'memprot_project'

	def ready(self):
		for i in range(10): 
			print('memprot_signals linked in')
		user_logged_in.connect(murder_console)
		email_confirmed.connect(murder_console)
		#user_signed_up.connect(garbage_fundion)