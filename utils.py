"""Misc stateless utility functions
"""


import os
import os.path
import io
import tempfile
from contextlib import contextmanager

import Bio.SeqIO

from flask import current_app as app
from itsdangerous import URLSafeSerializer

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

def read_env(fn='.env', dir=os.path.dirname(os.path.abspath(__file__))):
    """Read env file into environment, if found
    """
    envpath = os.path.join(dir, fn)
    env = {}
    if os.path.exists(envpath):
        with open(envpath, "r") as fh:
            for line in fh.readlines():
                if '#' not in line and '=' in line:
                    key, val = line.strip().split('=', 1)
                    # get rid of leading or trailing spaces or quotes
                    val = val.strip().strip("'").strip('"')
                    key = key.strip()
                    env[key] = val
                    os.environ[key] = val
    return env

def is_protein(seq):
    if seq.replace('A', '').replace('C', '').replace('G', '').replace('T', '') == '':
        return False
    else:
        return True

def parse_fasta(fn):
    for rec in Bio.SeqIO.parse(fn, "fasta"):
        yield rec.id, str(rec.seq)

def saniscript(POST, FILES):
    """Sanitize text or file input
    """
    sanitized = []
    if POST['protein'] == '':
        attachment = FILES.get('protein_file', False)
        for line in attachment:
            try:
                sanitized.append(str(line)[2:-2][:30])
                # sanitized.append(curate_sequence(str(line)))
            except TypeError:
                return ['']
        if sanitized != []:
            return sanitized
        else:
            return ['']
    else:
        try:
            sequence = (POST['protein'] + ' ').split('\n')
            [sanitized.append(line.rstrip()[:-3][:30] for line in sequence[:10])]
        except TypeError:
            return ['']
        # sequence = ml_utils.curate_sequence(sequence)
        return sequence


@contextmanager
def NamedTemporaryFile(*args, **kwargs):
    """Delete temporary file after exiting block (but not if closed)
    """
    if 'delete' in kwargs:
        kwargs.pop('delete')

    tf = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
    yield tf
    os.unlink(tf.name)


def mask_ip(addr):
    """Mask a given IP address to the beginning bit
    """
    if addr is None:
        return ''

    # ipv6 or IPv4 mapped IPv6
    if ':' in addr:
        data = addr.split(':', maxsplit=5)[:4]
        return "{}:{}:{}:{}:xxxx:xxxx:xxxx:xxxx".format(*data)
    # ipv4
    elif '.' in addr:
        data = addr.split('.', maxsplit=3)[:2]
        return "{}.{}.xxx.xxx".format(*data)
    else:
        return 'x' * len(addr)
    