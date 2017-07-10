from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_signed_up
from allauth.account.utils import complete_signup, perform_login

class AccountAdapter(DefaultAccountAdapter):
    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py
    def clean_password2(self, data):
        if ("password1" in data and "password2" in data):
            if (data["password1"] != data["password2"]):
                raise forms.ValidationError(("You must type the same password each time."))
            return data["password2"]


    # https://stackoverflow.com/questions/36488743/django-allauth-overriding-default-signup-form
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.username = data['username']
        user.institution = data['institution']
        user.email = data['email']
        user.website = data['website']
        if self.clean_password2(data):
            user.set_password(data['password2'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        complete_signup(
            request,
            user,
            'mandatory',
            '/'
            )
        print('beaglebeaglebeagle')
        return user