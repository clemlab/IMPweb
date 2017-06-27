# Imports all functions from funfile
# There should point to other functions elsewhere that perform calculations
from . import funfile
from .tasks import calculate_score
from .models import JobEntry

# Extracts information from a post and sanitized input
def email_script(user, POST, sanitized):
    test_list = [POST['your_email']]
    test_subject = POST['job_name']
    public = POST.get('display_mode', False)
    public = (public == 'On')
    if POST['method'] == 'length':
        test_fun = funfile.length
    elif POST['method'] == 'rev':
        test_fun = funfile.rev
    elif POST['method'] == 'spam':
        test_fun = funfile.spam
    else:
        raise ValueError("method not found: ", POST['method'])

    job = JobEntry()
    job.user_id = user
    job.job_name = test_subject
    job.job_email = test_list
    job.sanitized_input = sanitized
    job.is_public = public 
    job.save()
    # Adds the information to the queue
    calculate_score.delay(test_list, test_subject, test_fun, sanitized, job.job_id)
    return 'Your job will be processed shortly'


# WIP script to sanitize inputs
def saniscript(POST, FILES):
    sanitized = []
    if POST['protein'] == '':
        attachment = FILES.get('protein_file', False)
        for line in attachment:
            try:
                sanitized.append(str(line))
                # sanitized.append(curate_sequence(str(line)))
            except TypeError:
                return ['']
        if sanitized != []:
            return sanitized
        else:
            return ['']
    else:
        sequence = POST['protein']
        # sequence = ml_utils.curate_sequence(sequence)
        sanitized = [sequence]
        return sanitized
