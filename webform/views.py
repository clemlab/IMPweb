from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import django.contrib.auth as auth
from .form import SubmissionForm

from .script import email_script, saniscript

from .models import SubmissionEntry, JobEntry

from allauth.account.decorators import verified_email_required

def db_view(request, uuid=False):
    if not uuid:
        path = request.path_info
        uuid = path[16:-1]
    job = JobEntry.objects.get(job_id=uuid)
    results = job.output
    return render(request, 'results_template.html', {'results': results})


def results_table(request):
    table = JobEntry.objects.filter().order_by('date_completed')[:50]
    results = [result.output for result in table]
    return render(request, 'table.html', {'results': results})


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
            user = auth.get_user(request)
            status = email_script(str(user), request.POST, sanitized_input)
            return render(request, 'results.html', {'data': status})
    # If not it redirect to form
    else:
        return HttpResponseRedirect('/webform/')

@verified_email_required
def get_name(request):
    # if this is a POST request, we need to process it
    # the first part of the if statement is never called
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/webform/thanks/')
    else:
        form = SubmissionForm()

    return render(request, 'basic_input.html', {'form': form})


def profile(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if profile_form.is_valid():
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        #user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'user_profile.html',
                  {'profile_form': profile_form,
                   'registered': registered})
