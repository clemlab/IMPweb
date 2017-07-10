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



