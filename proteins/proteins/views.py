from django.http import HttpResponseRedirect, HttpResponse


def baseredirect(request):
	return HttpResponseRedirect('/form/')

def index(request):
	#test view
	return HttpResponse("something has gone right or wrong or something")