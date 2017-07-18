from django import forms
from inspect import getmembers, isfunction

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, ButtonHolder
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import UserProfile
from .adapter import AccountAdapter
from allauth.account.adapter import get_adapter


# Taken from allauth.account.forms to avoid cicular import
class PasswordVerificationMixin(object):
    def clean(self):
        cleaned_data = super(PasswordVerificationMixin, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if (password1 and password2) and password1 != password2:
            self.add_error(
                'password2', _("You must type the same password each time.")
            )
        return cleaned_data

#See mixin
class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value', '*')
        kwargs['widget'] = forms.PasswordInput(render_value=render_value,
                                               attrs={'placeholder': (kwargs.get("label"))})
        super(PasswordField, self).__init__(*args, **kwargs)


# Class for the login form
class LoginForm(forms.Form):
    # Forms for username and password
    username = forms.CharField(max_length=100)
    password = PasswordField(label="Enter your password")
    # Crispy forms stuff
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'password',
            )

    def login(self, request, user):
        '''
        Takes a request and a user and attempts to log user in.
        Returns the response that should be sent back to the client.
        '''
        from allauth.account.utils import perform_login
        response = perform_login(request, user, 'Mandatory')
        return response

    # More crispy forms stuff
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Login Form',
                'username',
                'password',
                ),
            FormActions(
                    ButtonHolder(
                    Submit('submit', 'Log in', css_class='button white')))
            )


# The class that handles the signup form
class UserProfileSignupForm(forms.Form):
    # The various fields users must enter data into
    username = forms.CharField(max_length=100)
    institution = forms.CharField(label='What institution do you work for?', max_length=100)
    email = forms.EmailField(label='Your email:', max_length=100)
    website = forms.URLField(label='What is your personal website?', required=False)
    password1 = PasswordField(label="Password")
    password2 = PasswordField(label="Password (again)")

    # Crispy forms stuff
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'institution',
            'email',
            'website',
            'password1',
            'password2',
            )

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py
    def clean_password2(self):
        '''
        Probably deprecated
        '''
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError(("You must type the same password each time."))
            return self.cleaned_data["password2"]

    def signup(self, request, user):
        '''
        Get the account adapter and save's the user
        '''
        adapter = get_adapter(request)
        test = adapter.save_user(request, user, self, commit=True)
        if not test:
            return False
        return True

    # Last bit of crispy stuff
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Signup Form',
                'username',
                'email',
                'institution',
                'website',
                'password1',
                'password2',
                ),
            FormActions(
                    ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')))
            )


class SocialUserSignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(label='Your academic email:', max_length=100)
    institution = forms.CharField(label='What institution do you work for?', max_length=100)
    website = forms.URLField(label='What is your personal website?', required=False)


    # Crispy forms stuff
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'email',
            'institution',
            'website',
            )


    def save(self, request):
        '''
        Get the account adapter and save's the user
        '''
        adapter = get_adapter(request)
        success = adapter.save_social_user(request, self.sociallogin, self, commit=True)
        if success:
            return
        return HttpResponse('Email not a valid academic email')


    # Last bit of crispy stuff
    def __init__(self, sociallogin=None, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.sociallogin = sociallogin
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Signup Form',
                'username',
                'email',
                'institution',
                'website',
                ),
            FormActions(
                    ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')))
            )   