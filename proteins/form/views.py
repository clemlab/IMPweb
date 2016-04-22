from django.shortcuts import render
from django.http import HttpResponseRedirect

from .form import NameForm

# Create your views here.
def index(request):
	return HttpResponse("something has gone wrong")

def get_name(request):
	#if this is a POST request, we need to process it
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/thanks/')
	else:
		form = NameForm()

	return render(request, 'name.html', {'form':form})