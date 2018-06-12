"""Web app for membrane protein expression prediction
"""

import os
import os.path
from io import TextIOWrapper

import flask
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mail import Message
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_restful import Api
from itsdangerous import BadSignature

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
import click

import pytest

from models import db, User, Batch, Score, Sequence
from tasks import rq, calculate_score, mail
# from rest import *
import utils

# Reads env file into environment, if found
_ = utils.read_env()

app = Flask(__name__)

if os.environ.get('IS_HEROKU', None):
    app.config['SERVER_NAME'] = os.environ['SERVER_NAME']
else:
    app.config['SERVER_NAME'] = 'localhost:5000'

# For data storage
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

# For job handling
app.config['RQ_REDIS_URL'] = os.environ['RQ_REDIS_URL']
rq.init_app(app)

# for author notification
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = os.environ['MAIL_DEFAULT_SENDER']
# https://technet.microsoft.com/en-us/library/exchange-online-limits.aspx
# 30 messages per minute rate limit
app.config['MAIL_MAX_EMAILS'] = 30
mail.init_app(app)

app.config['DEBUG'] = os.environ.get('DEBUG')

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)

api = Api(app)
# api.add_resource(TodoList, '/api/<string:api_key>/batch/string:<batch_payload>')
# api.add_resource(TodoList, '/api/<string:api_key>/batch/<string:batch_payload>/seq/<string:seq_id>')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webform', methods=['GET', 'POST'])
@app.route('/webform/basic', methods=['GET', 'POST'])
def submit():
    """Submit job
    protein jobs for nucleotide predictors get split up into different batches
    """
    if request.method == 'GET':
        return render_template('webform/basic_input.html',
            email=flask.session['user_email'] if flask.session.get('user_email') else "")

    email = request.form['email']
    user = User(email=email)
    user = db.session.merge(user)
    db.session.commit()

    batch = Batch(user_id=user.id, 
                  job_name=request.form['job_name'],
                  is_public=request.form['keeppublic'] == "on")
    batch = db.session.merge(batch)
    db.session.commit()
    
    # handle text area
    seq_objs = []
    sequence = request.form['sequence']
    if sequence != '':
        if '>'  in sequence:
            for name, seq in utils.parse_fasta(sequence):
                seq_objs += [Sequence(name=name, seq=seq)]
        else:
            seq_objs += [Sequence(name=batch.job_name, seq=sequence)]

    # handle uploaded file
    upfile = TextIOWrapper(request.files['sequencefile'])
    if upfile != '':
        for name, seq in utils.parse_fasta("".join(upfile)):
            seq_objs += [Sequence(name=name, seq=seq)]

    method = request.form['method']
    if method == 'improve_2018':
        method = 1
    else:
        raise ValueError("unknown method")

    for seq in seq_objs:
        seq = db.session.merge(seq)
        db.session.commit()
        
        score = Score(sequence_id=seq.id, predictor_id=method)
        score = db.session.merge(score)
        db.session.commit()

        batch.score.append(score)
        db.session.commit()

    db.session.commit()

    calculate_score.queue(batch, queue='impweb-' + user.priority)
    
    flash("Submitted {} sequences to queue. "
                "You should recieve an email when the batch has finished. "
                "Feel free to visit this page's URL to check on progress".format(len(seq_objs)))

    s = utils.get_serializer()
    return redirect(url_for("batch_data", batch_payload=s.dumps(batch.id)))

"""
#
#
# Results retrieval
# 
#
"""
@app.route('/public', methods=['GET'])
def public_results():
   # batch = Batch.query.limit(50).all()
    #if batch and batch.is_done:
    # table = Batch.query.order_by(Batch.date_entered.desc()).limit(50).all()
    table = Score.query.filter(Score.score.isnot(None)).order_by().limit(50).all()
    # else:
    #     table = None
    # for r in table:
    #     print(r.batch[0])

    return render_template('webform/table.html', results=table)


@app.route('/batch/<string:batch_payload>', methods=['GET'])
def batch_data(batch_payload=None):
    """Retrieve single batch results
    """
    s = utils.get_serializer()
    if batch_payload:
        try:
            batch_id = s.loads(batch_payload)
        except BadSignature:
            flash("That URL looks malformed. Please try clinking your link again.\n"
                        "Or contact the site administrator.")
            return redirect(url_for("submit"))

    batch = Batch.query.filter_by(id=batch_id).first()

    if batch and batch.is_done:
        table = BatchScore.query.filter_by(id=batch_id).all()
    else:
        table = None

    return render_template('webform/batch_table.html', table=table)

@app.route('/user/', methods=['GET'])
@app.route('/user/<string:user_payload>', methods=['GET'])
@app.route('/user/<string:user_payload>/batch/<string:batch_id>', methods=['GET'])
def user_data(user_payload=None, batch_id=None):
    """Retrieve user jobs
    If profile hasn't been filled out yet, then direct to profile page.
    """
    s = utils.get_serializer()
    if user_payload:
        try:
            user_email = s.loads(user_payload)
        except BadSignature:
            flash("Unrecognized URL. Please try clinking your link again.\n"
                  "Or contact the site administrator.")
            return redirect(url_for("submit"))

        # logged in user confirmed, now add to session
        flask.session['user_id'] = user_email
        flask.session['user_email'] = user_email
    elif flask.session.get('user_email'):
        # user already authenticated
        user_email = flask.session['user_email']
    else:
        flash("Please login to see your personal results")
        return redirect(url_for("public_results"))

    user = User.query.filter_by(email=user_email).first()
    if not user.institution:
        flash("Please fill in your information")
        return redirect(url_for("profile"))

    # if here, then either a valid batch_id alone,
    # a valid user_id with a batch_id, or just a valid user_id
    if batch_id:
        batch = Batch.query.filter_by(id=batch_id).first()

        if batch.is_done:
            table_data = Batch.query.filter_by(id=batch_id).all()
            return render_template('webform/batch_table.html', table=table_data)
        else:
            return render_template('webform/batch_table.html', table=None)
    else:
        # TODO: NEED TO CONNECT USERS TO BATCHES
        table_data = Batch.query.filter_by(id=batch_id).all()
        return render_template('webform/batch_table.html', table=table_data)


"""
#
#
# User Management
# 
#
"""

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('account/signup.html')

    user = User(email=request.form['email'])
    user = db.session.merge(user)
    db.session.commit()

    msg = Message("[IMPWEB] Login request",
                  recipients=[user.email, "clemlab@gmail.com"])
    msg.body = \
"""
Hello --

Thanks for your interest in IMProve.caltech.edu.
Click the below link to see all your jobs:

{}

Thanks,
IMProve team
""".format(user.url(_external=True))

    mail.send(msg)

    # send verification email with link to user_data: /user/<user_payload>
    flash("Please check your email to continue")

    return redirect('/webform')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Show/parse profile form for the currently logged-in user
    """
    if request.method == 'GET':
        if flask.session.get('user_email'):
            user = User.query.filter_by(email=flask.session['user_email']).first()
            return render_template('account/profile.html', user=user)
        else:
            flash("This URL cannot be accessed directly. "
                  "Try requesting a link to login below:")
            return redirect(url_for("signup"))

    # Proess submitted profile information
    user = User.query.filter_by(email=flask.session['user_email']).first()

    user.fullname = request.form['fullname']
    user.institution = request.form['institution']
    user.public_jobs = request.form['publicjobs'] == "on"

    user = db.session.merge(user)
    db.session.commit()
    print(user)

    return redirect(url_for("user_data"))

@app.route('/logout', methods=['GET'])
def logout():
    """
    Should we be cleanring 'user_id' and 'user_email' ... ?
    """
    user_id = flask.session.get('user_id')
    flask.session.clear()
    if user_id:
        flash("You have been successfully logged out")
    else:
        flash("Not logged in! (but the session has been cleared)")
    return redirect('/')

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash('CSRF Error. Try again?')
    return redirect('/')


@app.cli.command()
def orm():
    """Function to help test and debug ORM
    """
    user = User(email='smsaladi@gmail.com')
    user = db.session.merge(user)
    print('user:', user, 'num_b', len(user.batches))
    for b in user.batches:
        print('batch', b, 'len_s', len(b.scores))
        for s in b.scores:
            pred = s.predictor
            seq = s.sequence
            print('score', s, 'seq', seq, 'pred', pred)
            print(pred.scores)
            print(seq.id, seq.protein_id, seq.nuc_seqs)

    return


@app.cli.command()
def re_calculate_all():
    """Function to help test and debug ORM
    """
    user = User(email='smsaladi@gmail.com')
    user = db.session.merge(user)
    print('user:', user, 'num_b', len(user.batches))
    for b in user.batches:
        print('batch', b, 'len_s', len(b.scores))
        for s in b.scores:
            pred = s.predictor
            seq = s.sequence
            print('score', s, 'seq', seq, 'pred', pred)
            print(pred.scores)
            print(seq.id, seq.protein_id, seq.nuc_seqs)

    return

if __name__ == '__main__':
  app.run()
