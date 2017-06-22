from django import forms
from inspect import getmembers, isfunction



# All the possible functions for the drop-down menu
# Order is (function name, shown name)
# function name will be called later, so make sure it's correct
funs = [
    ('length', 'Length'),
    ('rev', 'Reverse'),
    ('spam', 'spam'),
]


class SubmissionForm(forms.Form):
    your_email = forms.EmailField(label='Your email:', max_length=100)
    job_name = forms.CharField(label='Job Name', max_length=50)
    protein = forms.CharField(widget=forms.Textarea, required=False)
    protein_file = forms.FileField(required=False)
    method = forms.ChoiceField(choices=funs, required=True )

    # forms.ValidationError("Need to provide an input")

    # def clean(self):
    #     print("got here")
    #     cleaned_data = super(SubmissionForm, self).clean()
    #
    #     cc_seqstr = cleaned_data.get("protein")
    #     cc_file = cleaned_data.get("protein_file")
    #
    #     print(cc_seqstr, cc_file)
    #
    #     if cc_seqstr is not None and cc_file is not None:
    #         raise forms.ValidationError("Need to provide an input")
    #     elif cc_seqstr and cc_file:
    #         raise forms.ValidationError("Only a sequence OR a file")
    #
    #     return


class UserProfileForm(forms.Form):
    your_email = forms.EmailField(label='Your email:', max_length=100)
    job_name = forms.CharField(label='Job Name', max_length=50)
    protein = forms.CharField(widget=forms.Textarea, required=False)
    # protein_name = forms.CharField(label = 'File name?', max_length = 50)
    protein_file = forms.FileField(required=False)
