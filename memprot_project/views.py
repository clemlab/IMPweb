from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


# def baseredirect(request):
#     return HttpResponseRedirect('/form/')


def index(request):
    return render(request, 'index.html')
