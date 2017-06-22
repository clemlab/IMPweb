from django.core.mail import send_mail, EmailMessage

from .tasks import calculate_score


def email_script(POST, sanitized):
    test_list = [POST['your_email']]
    test_subject = POST['job_name']
    calculate_score(test_list, test_subject, sanitized)
    return 'Your job will be processed shortly'


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
