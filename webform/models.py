import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User, UserManager
from django import forms
import datetime
import django
# All the possible functions for the drop-down menu
# Order is (function name, shown name)
# function name will be called later, so make sure it's correct
funs = [
    ('length', 'Length'),
    ('rev', 'Reverse'),
    ('spam', 'spam'),
]

class JobBatch(models.Model):
    batch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_name = models.CharField(max_length=50)
    is_public = models.BooleanField(default=True)
    job_email = models.EmailField(max_length=100)
    user_id = models.EmailField(max_length=100)
    batch_size = models.IntegerField(default=0)
    date_entered = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.job_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('job_view', args=[str(self.batch_id)])

    def output(self):
        return {
        'size': str(self.batch_size),
        'name': self.job_name,
        'date': str(self.date_entered.date()),
        'url': str(self.get_absolute_url()),
        }

class JobEntry(models.Model):
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(JobBatch, on_delete=models.CASCADE, null=True)
    batch_no = models.IntegerField(default=-1)
    sanitized_input = models.CharField(max_length=3000) 
    results = models.CharField(max_length=300, default='unfinished')
    date_started = models.DateTimeField(default=django.utils.timezone.now)
    date_completed = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.batch) + ' ' + str(self.batch_no)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('db_view', args=[str(self.job_id)])

    def output(self):
        return {
        'input': self.sanitized_input[:-1][:20],
        'output': self.results,
        'begin': str(self.batch.date_entered.date()),
        'end': str(self.date_completed - self.date_started),
        'url': str(self.get_absolute_url())
            }


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
