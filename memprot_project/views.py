from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import AbstractBaseUser
from .form import UserProfileSignupForm, LoginForm
from .models import UserProfile
# def baseredirect(request):
#     return HttpResponseRedirect('/form/')

# Basic dumb return of html page
def static_views(request):
    for page in ['publications', 'team', 'contact']:
        if page in request.path:
            return render(request, page + '.html')
    return render(request, 'index.html')

# Next step up the food chain. Logs out the user and redirects to index
def site_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

# Handles the signup form which redirects to the start of the if statement
def site_signup(request):
    # if this is a POST request, we need to process it
    # the first part of the if statement is never called
    # except after redirect
    if request.method == 'POST':
        form = UserProfileSignupForm(request.POST)
        if form.is_valid():
            # Creates a new user to be saved to database
            user = UserProfile()
            # Calls the signup method from form.py/userprofilesignupform
            success = form.signup(request, user)
            if success:
                return HttpResponseRedirect('/')
            return HttpResponse('Email not a valid academic email')

    else:
        # Makes a new form
        form = UserProfileSignupForm()
    # Renders the form
    return render(request, 'login_form.html', {'form': form})

# Handles the login form. Works essentially like signing up.
def site_login(request):
    # if this is a POST request, we need to process it
    # the first part of the if statement is never called
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # We need to fetch a preexisting user
            user = UserProfile.objects.get(username=form.cleaned_data['username'])
            response = form.login(request, user)
            return response
    else:
        form = LoginForm()

    return render(request, 'login_form.html', {'form': form})
