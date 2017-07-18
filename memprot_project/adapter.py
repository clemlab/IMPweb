from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import complete_signup
from .academic import acaemail_verify


class AccountAdapter(DefaultAccountAdapter):
    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py
    def clean_password2(self, data):
        '''
        Doublechecks the passwords provided so that they match
        '''
        if ("password1" in data and "password2" in data):
            if (data["password1"] != data["password2"]):
                raise forms.ValidationError(("You must type the same password each time."))
            return data["password2"]


    # https://stackoverflow.com/questions/36488743/django-allauth-overriding-default-signup-form
    def save_user(self, request, user, form, commit=False):
        '''
        Overrides the default user profile saving for our custom user profile
        Should take a blank user.
        '''
        # Gathers the data from the submitted form
        data = form.cleaned_data
        user.username = data['username']
        user.institution = data['institution']
        user.email = data['email']
        if not acaemail_verify(user.email.split('@')[1]):
            return False
        user.website = data['website']

        # Sets the password 
        if self.clean_password2(data):
            user.set_password(data['password2'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()

        # Allauth stuff that does our heavy lifting
        complete_signup(
            request,
            user,
            'mandatory',
            '/'
            )
        print('new user signed up')
        return user

    def save_social_user(self, request, sociallogin, form, commit=False):
        data = form.cleaned_data
        user = sociallogin.user
        user.username = data['username']
        user.institution = data['institution']
        user.email = data['email']
        if not acaemail_verify(user.email.split('@')[1]):
            return False
        user.website = data['website']

        if commit:
            sociallogin.save(request)

        complete_signup(
            request,
            user,
            None,
            '/')
        print('new social user signed up')
        return user