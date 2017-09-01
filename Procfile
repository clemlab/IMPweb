web: gunicorn memprot_project.wsgi --log-file -

worker: python manage.py rqworker high default low
