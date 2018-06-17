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
from werkzeug import secure_filename

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
import click

import pytest

from models import db, User, Batch, Sequence, Predictor # Score
from tasks import rq, calculate_score, mail

# from rest import *
import utils

# Reads env file into environment, if found
_ = utils.read_env()

app = Flask(__name__)
# limits uploads to 64 MB
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024

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

# functions to add to jinja
app.jinja_env.globals.update(mask_ip=utils.mask_ip)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webform', methods=['GET', 'POST'])
@app.route('/webform/basic', methods=['GET', 'POST'])
def basic():
    """Submit job
    protein jobs for nucleotide predictors get split up into different batches
    """
    if request.method == 'GET':
        return render_template('webform/basic_input.html',
            email=flask.session['user_email'] if flask.session.get('user_email') else "")

    email = request.form['email'].strip()
    user = User.query.filter_by(email=email).first()
    if user:
        user_id = user.id
    else:
        user = User(email=email)
        user = db.session.merge(user)
        db.session.commit()
        user_id = user.id

    print("user_id", user)

    # capture ip address in case of spam/other issues (Rosetta, others do this)
    # https://stackoverflow.com/a/49760261/2320823
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        # if behind a proxy
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.environ['REMOTE_ADDR']

    batch = Batch(user_id=int(user_id), 
                  job_name=request.form['job_name'],
                  submission_ip=ip,
                  is_public=request.form['keeppublic'] == "on")
    batch = db.session.merge(batch)

    db.session.commit()
    
    # handle text area
    seq_objs = []
    sequence = request.form['sequence'].strip()

    if sequence != '':
        if '>'  in sequence:
            for name, seq in utils.parse_fasta(sequence):
                seq_objs.append(Sequence(name=name, seq=seq, batch_id=batch.id, predictor_id=1))
        else:
            seq_objs.append(Sequence(name=batch.job_name, seq=sequence, batch_id=batch.id, predictor_id=1))

    upfile = request.files.get('sequencefile')
    if upfile:
        fn = "{}.fasta".format(batch.id)
        upfile.save(fn)
        for name, seq in utils.parse_fasta(fn):
            seq_objs += [Sequence(name=name, seq=seq, batch_id=batch.id, predictor_id=1)]
        os.unlink(fn)


    # method = request.form['method']
    # if method == 'improve_2018':
    #     method = 1
    # else:
    #     raise ValueError("unknown method")

    print(seq_objs)
    calculate_score.queue(batch, seq_objs, queue='impweb-med')
    
    flash("Submitted {} sequences to queue. "
                "You should receive an email when the batch has finished. "
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
    # table = (Batch.query
    #               .filter(Batch.is_public)
    #               .order_by(Batch.date_entered.desc())
    #               .limit(50)
    #               .all())
    # table = Batch.query.filter(Score.score.isnot(None)).order_by().limit(50).all()
    # else:
    #     table = None
    # for r in table:
    #     print(r.batch[0])
    flash("Something is broken - We are working on it!")
    return render_template('webform/table.html', results=None)


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
            return redirect(url_for("basic"))

    batch = Batch.query.filter_by(id=batch_id).first()

    if batch and batch.is_done:
        table = BatchScore.query.filter_by(id=batch_id).all()
    else:
        flash("Currently in the queue. We are working on it!")
        table = []

    return render_template('webform/table.html', table=table)



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
            return redirect(url_for("basic"))

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
    # if not user.institution:
    #    flash("Please fill in your information")
    #    return redirect(url_for("profile"))

    # if here, then either a valid batch_id alone,
    # a valid user_id with a batch_id, or just a valid user_id
    if batch_id:
        batch = Batch.query.filter_by(id=batch_id).first()

        if batch.is_done:
            table_data = Batch.query.filter_by(id=batch_id).all()
            return render_template('webform/table.html', table=table_data)
        else:
            flash("Currently in the queue (or something is broken). We are working on it!")
            return render_template('webform/table.html', table=None)
    else:
        # TODO: NEED TO CONNECT USERS TO BATCHES
        # table_data = Batch.query.filter_by(id=batch_id).all()
        flash("Currently in the queue (or something is wrong). We are working on it!")
        return render_template('webform/table.html', table=None)


@app.route('/families', methods=['GET'])
def families():
    flash("Sorry, we are currently working to make this available!")
    return redirect(url_for("basic"))

@app.route('/variants', methods=['GET', 'POST'])
def variants():
    flash("Sorry, we are currently working to make this available!")
    return redirect(url_for("basic"))

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

@app.cli.command()
@click.argument('allstats', required=True)
@click.argument('fna', required=False)
@click.argument('score', required=False)
@click.argument('jobname', required=False)
def load(allstats, fna=None, score=None, jobname=None, user_id=2):
    """Load precomputed scores into the database

    Assumes that fna and allstats are in the same order (if fna provided)

    cat microbial_query.tsv | tail -n+2 | awk '{print ">"$1"|"$2"|"$3"|"$4"|"$5" "$6"\n"$(NF)}' > microbial_query.fna
    """

    import pandas as pd
    import Bio.SeqIO

    df_feat = pd.read_csv(allstats)
    feat_cols = [c for c in df_feat.columns.tolist() if c not in ['title']]
    
    df_feat.set_index('title', inplace=True)

    if fna:
        seqs = list(Bio.SeqIO.parse(fna, 'fasta'))
        
        df_seq = pd.DataFrame({'nucseq': [str(r.seq) for r in seqs]},
                              index=[r.id for r in seqs])
        # reindex becuase the names in allstats could be truncated
        df_feat.index = df_seq.index

        df_feat = pd.concat([df_seq, df_feat], axis=1, copy=False, sort=False)
    else:
        assert 'nucseq' in df_feat.columns

    if score:
        df_score = pd.read_csv(score, header=None, names=['score'])
        df_score.index = df_feat.index
        df_feat = pd.concat([df_feat, df_score], axis=1, copy=False, sort=False)
    else:
        assert 'score' in df_feat.columns

    if jobname is None:
        jobname = os.path.basename(allstats)
        for ext in ['fna', 'allstats', 'csv', 'gz']:
            jobname = jobname.replace('.' + ext, '')

    # user = User(email=email)
    # user = db.session.merge(user)
    batch = Batch(user_id=user_id, job_name=jobname, is_done=True)
    batch = db.session.merge(batch)
    pred = Predictor(name='improve_2018_nornass')
    pred = db.session.merge(pred)
    db.session.commit()
    print(batch, pred)
    
    # keep only polytopic imps
    print(df_feat.shape)
    df_feat = df_feat[df_feat['numTMs'] > 1]
    print(df_feat.shape)

    # prep data
    def pd_translate(x):
        prot = Bio.Seq.Seq(x, Bio.Seq.Alphabet.generic_dna).translate()
        return str(prot)
    def pd_hash(x):
        return Sequence.to_id(x)

    df_feat['protseq'] = df_feat['nucseq'].map(pd_translate)
    df_feat['nuc_id'] = df_feat['nucseq'].map(pd_hash)
    df_feat['prot_id'] = df_feat['protseq'].map(pd_hash)

    print(df_feat.shape)
    df_feat.drop_duplicates(subset=['nuc_id'], inplace=True)
    print(df_feat.shape)

    def rm_nuc(x):
        return x.str.contains('N') | (x.str.len() % 3 != 0)
    def rm_prot(x):
        return x.str.contains('X') | (x.str[:-1].str.contains('*', regex=False))
    # drop if sequence is not well formed
    rm = rm_nuc(df_feat['nucseq']) | rm_prot(df_feat['protseq'])
    df_feat = df_feat[~rm]


    def to_data(x, feats):
        return x[feats].to_json()
    df_feat['data'] = df_feat.apply(to_data, axis=1, feats=feat_cols)

    # # Sequence
    # df_feat[['prot_id', 'name', 'protseq']].to_csv(
    #     "Sequence.prot_{}".format(jobname), sep="\t", header=None, index=False)
    # df_feat[['nuc_id', 'name', 'nucseq']].to_csv(
    #     "Sequence.prot_{}".format(jobname), sep="\t", header=None, index=False)
    
    # # Score
    # df_feat[['nuc_id', 'data', 'score']].to_csv(
    #     "Score.{}".format(jobname), sep="\t", header=None, index=False
    # )

    print(df_feat.shape)

    # insert prot separatly
    df_prot = df_feat[['protseq']].drop_duplicates()
    print(df_prot.shape)
    for idx, data in enumerate(df_prot.iterrows()):
        name, row = data
        prot = Sequence(seq=row['protseq'], name=name, batch_id=batch.id)
        db.session.add(prot)
        if idx % 1000 == 999:
            db.session.commit()

    db.session.commit()
    print(batch)

    # now insert nuc into db
    for idx, data in enumerate(df_feat.iterrows()):
        name, row = data
        
        nuc = Sequence(seq=row['nucseq'], name=name, batch_id=batch.id, predictor_id=pred.id,
                        score=row['score'], data=row['data'], protein_id=prot.id)       
        db.session.add(nuc)
        if idx % 1000 == 999:
            db.session.commit()

    db.session.commit()
    print(batch)

if __name__ == '__main__':
  app.run()
