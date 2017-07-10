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



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = PasswordField(label="Enter your password")
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'password',
            )

    def login(self, request, user):
        from allauth.account.utils import perform_login
        response = perform_login(request, user, None)
        return response

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



class UserProfileSignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    institution = forms.CharField(label='What institution do you work for?', max_length=100)
    email = forms.EmailField(label='Your email:', max_length=100)
    website = forms.URLField(label='What is your personal website?', required=False)
    password1 = PasswordField(label="Password")
    password2 = PasswordField(label="Password (again)")

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
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError(("You must type the same password each time."))
            return self.cleaned_data["password2"]

    def signup(self, request, user):
        adapter = get_adapter(request)
        adapter.save_user(request, user, self, commit=True)
        return

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

