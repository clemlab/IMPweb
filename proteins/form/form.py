from django import forms

class SubmissionForm(forms.Form):
	your_email = forms.CharField(label = 'Your email:', max_length = 100)
	job_name = forms.CharField(label = 'Job Name', max_length = 50)
	protein = forms.CharField(label = 'DNA Sequence?', max_length = 2000)
	#protein_name = forms.CharField(label = 'File name?', max_length = 50)
	protein_file = forms.FileField()