from memprot_project.celery import app

from django.core.mail import send_mail, EmailMessage

# import single_calc


@app.task
def calculate_score(test_list, test_subject, sanitized):
    body = 'This email is to confirm a successful test\n'
    sender = 'cnelson.django.test@gmail.com'
    results = open('results.txt', 'w')
    for element in sanitized:
        # results.write(single_calc.get_score(element))
        results.write(len(element))
        results.write('\n')
    results.close()
    test_message = 'file attached'
    email = EmailMessage(test_subject + ' test results', body, sender,
                         test_list)
    email.attach_file('results.txt')
    email.send(fail_silently=False)
    return 'your email has been sent'
