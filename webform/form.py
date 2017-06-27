from django import forms
from inspect import getmembers, isfunction

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, ButtonHolder
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import SubmissionEntry, funs




class SubmissionForm(forms.ModelForm):
    your_email = forms.EmailField(label='Your email:', max_length=100)
    job_name = forms.CharField(label='Job Name', max_length=50)
    protein = forms.CharField(widget=forms.Textarea, required=False)
    protein_file = forms.FileField(required=False)
    method = forms.ChoiceField(choices=funs, required=True)
    display_mode = forms.BooleanField(label='Display publically?', required=False)    

    
    class Meta:
        model = SubmissionEntry
        fields = (
            'your_email',
            'job_name',
            'protein',
            'protein_file',
            'method',
            'display_mode',
            )



    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Submission Form',
                'your_email',
                'job_name',
                'protein',
                'protein_file',
                'method',
                'display_mode',
                ),
            FormActions(
                    ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')))
            )




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
