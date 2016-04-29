from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .form import NameForm

from .script import silly_script, saniscript


# Create your views here.
def index(request):
	#test view
	return HttpResponse("something has gone right or wrong or something")

def thanks(request):
	#if it receives a post from get_name, it returns the reverse of the 
	#your_name string.
	if request.method == 'POST':
		return HttpResponse(saniscript(request.POST['your_name']))
	#If not it redirect to form
	else:
		return HttpResponseRedirect('/form/')

def formredirect(request):
	return HttpResponseRedirect('/form/')


def get_name(request):
	#if this is a POST request, we need to process it
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/form/thanks/')
	else:
		form = NameForm()

	return render(request, 'form/name.html', {'form':form})