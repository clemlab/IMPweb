from django.core.mail import send_mail, EmailMessage
import re
import os

from .tasks import calculate_score

def email_script(POST, sanitized):
	test_list = [POST['your_email']]
	test_subject = POST['job_name']
	calculate_score.apply_async((test_list, test_subject, sanitized), 
		queue='celery')
	return 'Your job will be processed shortly'

def silly_script(string):
	return string[::-1]

def saniscript(POST, FILES):
	sanitized = []
	if POST['protein'] == '':
		attachment = FILES.get('protein_file', False)
		for line in attachment:
			try:
				sanitized.append(curate_sequence(str(line)))
			except TypeError:
				return ['']
		if sanitized != []:
			return sanitized
		else:
			return ['']
	else:
		sequence = POST['protein']
		sequence = curate_sequence(sequence)
		sanitized = [sequence]
		return sanitized

def curate_sequence(seq, nucleotide=True, keep_register=False):
    """Removing non-standard characters from a sequence
    Parameters
    ----------
    seq : str
    nucleotide : Optional[bool]
        Should the sequence should be interpreted as a nucleotide sequence or
        not (i.e. as a protein sequence)?
    keep_register : Optional[bool]
        Should the sequence register be retained when removing unknown
        characters? If so, unknown characters are replaced by `X`.
    Returns
    -------
    str
        The sequence with unacceptable characters removed
    Raises
    ------
    None
    """
    seq = seq.upper()
    bytes(seq, 'utf-8')
    if nucleotide:
        seq = seq.replace('U', 'T')
        re_remove = re.compile('[^ATGCU]')
    else:
        re_remove = re.compile('[^ACDEFGHIKLMNPQRSTVWY]')

    if keep_register:
        return re_remove.sub('X', seq)
    else:
        return re_remove.sub('', seq)



