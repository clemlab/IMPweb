from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout


# def baseredirect(request):
#     return HttpResponseRedirect('/form/')


def index(request):
    return render(request, 'index.html')

def site_logout(request):
	logout(request)
	return HttpResponseRedirect('/')