"""Here is the interface that calls the backend code for calculations
"""

import sys
import re
import os
import datetime
import subprocess
import io
import tempfile

import pytest
from flask_rq2 import RQ
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

try:
    import pandas as pd
    import Bio.Seq
    import Bio.Alphabet
    import Bio.SearchIO
except ImportError:
    print("Calculations will fail if this is a worker", file=sys.stderr)


from models import *

rq = RQ()
mail = Mail()
db = SQLAlchemy()

def test_detect_pfam():
    with open("scan2.out", "r") as fh:
        data = fh.read()

    r = io.StringIO(data)

    q = list(Bio.SearchIO.parse(r, "hmmer3-text"))

    print(q)
    return

def detect_pfam(prot):
    """Detect pfam domains for a single protein input
    """
    return ""
    prot = Bio.Seq.Seq(prot, Bio.Alphabet.generic_protein)
    rec = Bio.SeqRecord.SeqRecord(name="scan", seq=prot)

    with subprocess.Popen(['hmmscan', 'HMM', '-',
                           '--noali', '--notextw', '--cut_tc', '--max'],
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE) as p:
        result = p.communicate(input=rec.format("fasta"))

    # should only be one match in the file
    qresult = list(SearchIO.parse(io.StringIO(result), 'hmmer3-tab'))[0]
    hits = pd.DataFrame([[h.id, h.bitscore] for h in qresult.hits],
                        columns=['id','bitscore'])
    return hits.to_json()

def is_protein(seq):
    return len(re.sub('[ACGT]', '', seq)) > 0

def check_sequence(seq):
    """Takes a string and checks to validate sequence
    # * Javascript input santization?
    # * Detect dont run sequence, just send email
    # * If sequence is too long, warn user, and dont run RNA folding calculations
    """
    seq = seq.upper()
    clean = re.sub('[ARNDCEQGHILKMFPSTWYV]', '', seq.upper())
    if len(clean) > 0:
        return False, "Unknown characters"

    prot = seq

    if not is_protein(prot):
        # check length
        if len(seq) % 3 != 0:
            return False, "Length needs to be a multiple of 3"

        # check premature stop
        prot = Bio.Seq.Seq(seq, Bio.Seq.Alphabet.generic_dna).translate()
        if '*' in prot[:-1]:
            return False, "Premature stop detected"

    # check that polytopic
    # not IMP, dont run, suggest other software
    # if numTMs <= 1:
    #    return False, "Needs to be polytopic"

    # Detect Pfam(s)
    pfam = detect_pfam(prot)
    return True, pfam


def find_coding_seqs(seq):
    """
    * Protein to Nuc
    * Implement pipeline to run diamond with protein sequences to pick up all coding seqs
    """
    with utils.NamedTemporaryFile() as fh:
        fh.write(seq.format("fasta"))
        fh.close()
        subprocess.call([
            'mmseqs', 'search',
            fh.name, '~/db/ncbi/genomes/mmdb/GCF_CDS', 'fh.name' + '_alndb', '~/tmp/',
            '-s', '1', '--min-ungapped-score', '50', '-c', '.9'
        ])
    return

@rq.job('impweb-med', timeout='10m')
def calculate_score(batch, seqs, notify=False, force=False):
    """Calculate scores for all sequences in a batch
    
    * Assuming that all data in a batch wants the same predictor
    * Check if sequence is too long, warn user, and dont run RNA folding calculations
    """

    batch = db.session.merge(batch)
    print(batch.user)

    seq_calc = {}
    # check if already exists in database
    for s in seqs:
        prev_seq = Sequence.query.filter_by(id=s.id).first()
        if not force and prev_seq:
            s.score = prev_seq.score
            s.data = prev_seq.data
            s.error = prev_seq.error
            s.protein_id = prev_seq.protein_id
            print("sequence already calculated")
        elif is_protein(s.seq):
            s.error = "NO PROTEINS"
            print("no proteins yet")
        else:
            seqok, msg = check_sequence(s.seq)
            if seqok:
                s.pfam = msg
                seq_calc[s.id] = s
            else:
                s.error = msg

        s = db.session.merge(s)
        batch.sequences.append(s)
        db.session.commit()

    if not batch.date_started:
        batch.date_started = datetime.utcnow()

    print(seq_calc)

    if len(seq_calc) > 0:
        with tempfile.TemporaryDirectory() as td:
            fn = os.path.join(td, str(batch.id) + '.fna')
            with open(fn, 'w') as fh:
                for seq in seq_calc.values():
                    # keep these objects to make it easy to commit back the scores after calculation
                    print(">{}\n{}".format(seq.id, seq.seq), file=fh)

            # calculate slow features
            subprocess.call(["/ul/saladi/github/ml-expression_improve/scripts/master_precalc.pbs", fn])

            # calculate rest of features and score
            subprocess.call(["/ul/saladi/github/ml-expression_improve/scripts/master.sh", fn])

            # parse files
            df_feats = pd.read_csv(fn + '.allstats.csv')
            df_scores = pd.read_csv(fn + '.allstats.ml21', header=None, names=['score'])

        df_feats = pd.concat([df_feats, df_scores], axis=1, ignore_index=True)

        # add scores and features to database
        for _, row in df_feats.iterrows():
            name = row['title']
            # codonw truncates the name at like 30 characters or something
            for k in seq_calc.keys():
                if k.startswith(name):
                    name = k
                    break
                else:
                    print("Not found in calculation output", name, file=sys.stderr)

            seq = seq_calc[name]
            seq.score = row['score']
            seq.data = row.to_json()

            # commit back to database
            # might be able to do this all at once
            seq = db.session.merge(seq)
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

Thanks for your interest in IMProve.caltech.edu.
Your job seems to have completed.

Please visit:

{}

IMProve team
""".format(batch.user.url(batch.id))

    mail.send(msg)
    return
