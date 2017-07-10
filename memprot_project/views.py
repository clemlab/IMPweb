from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import AbstractBaseUser
from .form import UserProfileSignupForm, LoginForm
from .models import UserProfile
# def baseredirect(request):
#     return HttpResponseRedirect('/form/')


def index(request):
    return render(request, 'index.html')

def site_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def site_signup(request):
    # if this is a POST request, we need to process it
    # the first part of the if statement is never called
    if request.method == 'POST':
        form = UserProfileSignupForm(request.POST)
        if form.is_valid():
            user = UserProfile()
            form.signup(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserProfileSignupForm()

    return render(request, 'login_form.html', {'form': form}, {'redirect': 'signup'})

def site_login(request):
    # if this is a POST request, we need to process it
    # the first part of the if statement is never called
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = UserProfile.objects.get(username=form.cleaned_data['username'])
            response = form.login(request, user)
            return response
    else:
        form = LoginForm()

    return render(request, 'login_form.html', {'form': form})