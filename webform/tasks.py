from django.core.mail import send_mail, EmailMessage
from time import sleep


# Imports all functions from funfile
# There should point to other functions elsewhere that perform calculations
from .funfile import *




def calculate_score(test_list, test_subject, fun, sanitized):
    body = 'This email is to confirm a successful test\n'
    sender = 'cnelson.django.test@gmail.com'
    results = open('results.txt', 'w')
    for element in sanitized:
        # Evaluate the function chosen by the user with the given arg
        results.write(str(globals()[fun](element)))
        results.write('\n')
    results.close()
    # Emails out the results
    email = EmailMessage(test_subject + ' test results', body, sender,
                         test_list)
    email.attach_file('results.txt')
    email.send(fail_silently=False)
    return 'your email has been sent'
