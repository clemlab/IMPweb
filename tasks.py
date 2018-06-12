"""Here is the interface that calls the backend code for calculations
"""

import sys
import os
import datetime
import subprocess
import tempfile

import pytest
from flask_rq2 import RQ
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

try:
    import pandas as pd
except ImportError:
    print("Calculations will fail if this is a worker", file=sys.stderr)


from models import *

rq = RQ()
mail = Mail()
db = SQLAlchemy()

def check_sequence(seq):
    # check that polytopic
    # check premature stop
    # check N if nucleotide

    # check X if protein

    # Detect Pfam(s)


    # * Sanitization
    # * Javascript input santization?
    # * Minimum length?
    # * Detect premature stop, ambig nucs and dont run sequence, just send email
    # * not IMP, dont run, suggest other software
    # * If sequence is too long, warn user, and dont run RNA folding calculations
    # * Detect Pfam(s) automatically?


    return

def find_coding_seqs():
    """
    * Protein to Nuc
    * Implement pipeline to run diamond with protein sequences to pick up all coding seqs
    """

@rq.job('impweb-med', timeout='10m')
def calculate_score(batch, notify=True, force=False):
    """Calculate scores for all sequences in a batch
    subprocess.call("./test.sh
    Assuming that all data in a batch has the same predictor
    
    
    * Check if sequence is too long, warn user, and dont run RNA folding calculations

    """
    batch = db.session.merge(batch)

    if not batch.date_started:
        batch.date_started = datetime.utcnow()

    # all seqs in a batch should have the same predictor
    pred = batch.scores[0].predictor

    score_objs = {}

    with tempfile.TemporaryDirectory() as td:
        fn = os.path.join(td, str(batch.id) + '.fna')
        with open(fn, 'w') as fh:
            for scr in batch.scores:
                # only add for calculation if score is not present (or forced)
                if force or not scr.score:
                    seq = scr.sequence
                    # keep these objects to make it easy to commit back the scores after calculation
                    score_objs[seq.id] = scr
                    print(">{}\n{}".format(seq.id, seq.seq), file=fh)

        # calculate slow features
        subprocess.call(["/ul/saladi/github/ml-expression_improve/scripts/master_precalc.pbs", fn])

        # calculate rest of features and score
        subprocess.call(["/ul/saladi/github/ml-expression_improve/scripts/master.sh", fn])

        # parse files
        df_feats = pd.read_csv(fn + '.allstats.csv')
        df_scores = pd.read_csv(fn + '.allstats.ml21', header=None, names=['score'])

    df_feats = pd.concat([df_feats, df_scores], axis=1)

    # add scores and features to database
    for _, row in df_feats.iterrows():
        name = row['title']
        # codonw truncates the name at like 30 characters or something
        for k in score_objs.keys():
            if k.startswith(name):
                name = k
                break
            else:
                print("Not found in calculation output", name, file=sys.stderr)

        cur_scr = score_objs[name]
        cur_scr.score = row['score']
        cur_scr.data = row.to_json()

        # commit back to database
        cur_scr = db.session.merge(cur_scr)
        db.session.commit()

    # batch is now done
    batch.date_completed = datetime.utcnow()
    if notify:
        batch_notification(batch)

    return

def batch_notification(batch):
    msg = Message("[IMPWEB] Job `{}` has completed".format(batch.job_name),
                  recipients=[batch.user.email, "clemlab@gmail.com"])
    msg.body = \
"""
Hello --

Thanks for your interest in IMProve.caltech.edu. Your job has completed.
Please visit:

{}

IMProve team
""".format(batch.user.url(batch.id))

    mail.send(msg)
    return
