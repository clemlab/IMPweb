from django.apps import AppConfig
from django.core.signals import request_finished
from django.contrib.auth.signals import user_logged_in as django_login
from allauth.account.signals import user_signed_up, user_logged_in


from .signals import murder_console

class ProjectConfig(AppConfig):
	name = 'memprot_project'

	def ready(self):
		for i in range(10): 
			print('argle bargle')
		user_logged_in.connect(murder_console)
		#user_signed_up.connect(garbage_fundion)