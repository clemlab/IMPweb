import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User, UserManager
from django import forms

# All the possible functions for the drop-down menu
# Order is (function name, shown name)
# function name will be called later, so make sure it's correct
funs = [
    ('length', 'Length'),
    ('rev', 'Reverse'),
    ('spam', 'spam'),
]

class JobEntry(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.EmailField(max_length=100)
    job_email = models.EmailField(max_length=100)
    job_name = models.CharField(max_length=50)
    sanitized_input = models.CharField(max_length=3000) 
    is_public = models.BooleanField()
    results = models.CharField(max_length=300)

    def __str__(self):
        return self.job_name 

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('db_view', args=[str(self.job_id)])

    def output(self):
        return str(self.user_id) + '\n' + str(self.job_email) + '\n' + \
            str(self.job_name) + '\n' + self.sanitized_input + \
            str(self.is_public) + '\n' + str(self.results)


class SubmissionEntry(models.Model):
    your_email = forms.EmailField(label='Your email:', max_length=100)
    job_name = forms.CharField(label='Job Name', max_length=50)
    protein = forms.CharField(widget=forms.Textarea, required=False)
    protein_file = forms.FileField(required=False)
    method = forms.ChoiceField(choices=funs, required=True)
    display_mode = forms.BooleanField(label='Display publically?', required=False)



'''
class Seq(models.Model):
    seqid = models.TextField()
    nucseq = models.TextField()

    def __str__(self):
        return self.nucseq


class Predictor(models.Model):
    name = models.TextField()
    desc = models.TextField()

    def __str__(self):
        return self.name


class SeqPred(models.Model):
    user = models.ForeignKey(UserProfile)
    seq = models.ForeignKey(Seq)
    pred = models.ForeignKey(Predictor)

    views = models.IntegerField(default=0)

    def __str__(self):
        return "{user}_{seq}_{pred}".format(
            UserProfile, Seq, Predictor)

'''
