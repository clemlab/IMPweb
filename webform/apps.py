from django.apps import AppConfig
from django.core.signals import request_finished
from allauth.account.signals import user_signed_up, user_logged_in


#from .signals import murder_console

class FormConfig(AppConfig):
    name = 'form'

    def ready(self):
    	pass
    	#user_signed_up.connect(murder_console)
