import os
import time
import tempfile
from contextlib import contextmanager

from django.conf import settings
from django.core.mail import EmailMessage

from django_rq import job
from .models import JobEntry

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
    body = 'This email is to confirm a successful test\n'
    sender = settings.EMAIL_HOST_USER

    # delay for testing django_rq
    time.sleep(10)

    # set up results notification
    email = EmailMessage(test_subject + ' test results',
                         body,
                         sender,
                         test_list)

    with NamedTemporaryFile('w', suffix='.txt') as tf:
        for element in sanitized:
            # Evaluate the function chosen by the user with the given arg
            print(fun(element), file=tf)

        
        tf.close()
        email.attach_file(tf.name)

        email.send(fail_silently=False)

        job = JobEntry.objects.get(job_id=jobid)
        print(jobid)
        job.results = tf
        job.save

    return 'your email has been sent'
