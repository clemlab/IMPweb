import os
import time
import tempfile
import datetime

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
    job = JobEntry.objects.get(job_id=jobid)
    body = 'This email is to confirm a successful test \n \
    Your job url is: http://127.0.0.1:8000'  + str(job.get_absolute_url())
    sender = settings.EMAIL_HOST_USER

    # delay for testing django_rq
    #time.sleep(10)

    # set up results notification
    email = EmailMessage(test_subject + ' test results',
                         body,
                         sender,
                         test_list)

    results = []
    with NamedTemporaryFile('w', suffix='.txt') as tf:
        for element in sanitized:
            result = fun(element)
            # Evaluate the function chosen by the user with the given arg
            print(result, file=tf)
            results.append(result)
        
        tf.close()
        job.results = str(results)
        job.date_completed = datetime.datetime.now()
        job.save()
        email.attach_file(tf.name)

        email.send(fail_silently=False)

        

    return 'your email has been sent'
