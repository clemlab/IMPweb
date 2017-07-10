#from allauth.account.utils import send_email_confirmation


def murder_console(sender, **kwargs):
	for i in range(100):
		print('koszonom!')

def garbage_fundion(sender, request=False, user=False, **kwargs):
	if not user or not request:
		return
	#send_email_confirmation(request, user, signup=True)
	return
