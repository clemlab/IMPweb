import os
import time
import tempfile
import datetime

from contextlib import contextmanager

from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from django_rq import job
from .models import JobEntry, JobBatch
from django.utils import timezone

@contextmanager
def NamedTemporaryFile(*args, **kwargs):
    """Delete temporary file after exiting block (but not if closed)
    """
    if 'delete' in kwargs:
        kwargs.pop('delete')

    tf = tempfile.NamedTemporaryFile(*args, **kwargs, delete=False)
    yield tf
    os.unlink(tf.name)

@job
def calculate_score(test_list, test_subject, fun, sanitized, jobid):
    batch = JobBatch.objects.get(batch_id=jobid)

    results = []
    for index, task in enumerate(sanitized):
        job = JobEntry()
        job.batch = batch
        job.batch_no = index + 1
        job.sanitized_input = task
        job.results = str(fun(task))
        # delay for testing django_rq
        time.sleep(4)
        job.date_completed = timezone.now()
        job.save()
        results.append(task + ': ' + job.results)

    mail = EmailMultiAlternatives(
      subject="Your Subject",
      body=('This email is to confirm a successful test\n'
            'Your job url is: http://127.0.0.1:8000') + str(batch.get_absolute_url()),
      from_email="Shyam Saladi <saladi@caltech.edu>",
      to=test_list,
      reply_to=["saladi@caltech.edu"]
    )
    # Add template
    # mail.template_id = 'YOUR TEMPLATE ID FROM SENDGRID ADMIN'

    # Replace substitutions in sendgrid template
    # mail.substitutions = {'%username%': 'elbuo8'}

    # Attach file
    mail.attach_alternative("\n".join(results), "text/plain")

    mail.send(fail_silently=False)
    return 'your email has been sent'
