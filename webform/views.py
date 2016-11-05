from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .form import SubmissionForm

from .script import email_script, saniscript


# Create your views here.
def index(request):
    # test view
    return HttpResponse("something has gone right or wrong or something")


def thanks(request):
    # if it receives a post from get_name, it spams some poor soul's email
    if request.method == 'POST':
        sanitized_input = saniscript(request.POST, request.FILES)
        if sanitized_input == ['']:
            return HttpResponse('Error in data given.')
        else:
            for element in sanitized_input:
                if len(element) <= 30:
                    return HttpResponse('some input too short')
            return HttpResponse(email_script(request.POST, sanitized_input))
    # If not it redirect to form
    else:
        return HttpResponseRedirect('/form/')


def get_name(request):
    # if this is a POST request, we need to process it
    # the first part of the if statement is never called
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/form/thanks/')
    else:
        form = SubmissionForm()

    return render(request, 'basic_input.html', {'form': form})
