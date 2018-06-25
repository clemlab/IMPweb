import json
import hashlib
from datetime import datetime

import flask


import sqlalchemy.types as types
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy

import utils
from utils import get_serializer

db = SQLAlchemy()

class StrippedString(types.TypeDecorator):
    """A string that strips whitespace before and after when assigned

    Processing takes place when the value is to be bound to a query as
    a parameter, i.e. after db.session.commit

    https://stackoverflow.com/a/50854876/2320823
    """
    impl = db.String
    def process_bind_param(self, value, dialect):
        if value:
            # if None, then obviously, don't strip
            return value.strip()
        return value
    def copy(self, **kw):
        return StrippedString(self.impl.length)



# batch_score = db.Table(
#     'batch_scores', 
#     db.Column('batch_id', db.Integer, db.ForeignKey('batches.id'),
#               primary_key=True, nullable=False),
#     db.Column('score_id', db.Integer, db.ForeignKey('scores.id'),
#               primary_key=True, nullable=False),
# )

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True)
    id = db.Column(db.Integer, nullable=False, autoincrement=True)
    fullname = db.Column(StrippedString(100), nullable=True)
    institution = db.Column(StrippedString(100), nullable=True)

    public_jobs = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # low, medium, high
    _priority = db.Column('priority', db.String, default='low')

    # when this is "lazy", querying doesn't work for some reason
    batches = db.relationship('Batch', backref='user', lazy="noload", innerjoin=True)

    @hybrid_property
    def priority(self):
        return self._priority
    @priority.setter
    def priority(self, data):
        if data in ['low', 'medium', 'high']:
            self._priority = data
        else:
            raise ValueError('Unsupported priority', data)

    def __repr__(self):
        return json.dumps({c.name: getattr(self, c.name) for c in self.__table__.columns}, default=str)

    def url(self, batch_id=None, **kwargs):
        ser = get_serializer()
        if batch_id:
            return flask.url_for('user_data', user_payload=ser.dumps(self.email), batch_id=batch_id, **kwargs)            
        else:
            return flask.url_for('user_data', user_payload=ser.dumps(self.email), **kwargs)

class Batch(db.Model):
    __tablename__ = 'batches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)    
    job_name = db.Column(StrippedString(50))
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    
    is_done = db.Column(db.Boolean, default=False, nullable=False)
    submission_ip = db.Column(StrippedString(50), nullable=True)
    date_entered = db.Column(db.DateTime, default=datetime.utcnow)
    date_started = db.Column(db.DateTime, default=None)
    date_completed = db.Column(db.DateTime, default=None)

    sequences = db.relationship('Sequence', backref='batch')

    def __repr__(self):
        return json.dumps({c.name: getattr(self, c.name) for c in self.__table__.columns}, default=str)

    def url(self):
        ser = get_serializer()
        return flask.url_for('batch_data', batch_payload=ser.dumps(self.id))


class Predictor(db.Model):
    __tablename__ = 'predictors'
    name = db.Column(StrippedString(100), primary_key=True, nullable=False)
    id = db.Column(db.Integer, autoincrement=True, nullable=False)
    protein_only = db.Column(db.Boolean, nullable=False)

    sequences = db.relationship('Sequence', backref='predictor', lazy=True)

    def __repr__(self):
        return json.dumps({c.name: getattr(self, c.name) for c in self.__table__.columns}, default=str)

# sequence_translation = db.Table(
#     'sequence_translations', 
#     db.Column('prot_id', db.String(32), db.ForeignKey('sequence.id'), nullable=False),
#     db.Column('nuc_id', db.String(32), db.ForeignKey('sequence.id'), nullable=False),
#     db.PrimaryKeyConstraint('prot_id', 'nuc_id')
# )

class Sequence(db.Model):
    __tablename__ = 'sequences'
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(StrippedString(100))
    _seq = db.Column('seq', db.Text, nullable=False)

    # batch related info
    batch_id = db.Column(db.Integer, db.ForeignKey(Batch.id), nullable=True, primary_key=True)
    
    # score related items
    predictor_id = db.Column(db.Integer, db.ForeignKey(Predictor.id), nullable=True)
    score = db.Column(db.Float, nullable=True)
    data = db.Column(db.Text, nullable=True)
    pfam = db.Column(db.Text, nullable=True)
    error = db.Column(StrippedString(100), nullable=True)

    # connects coding with protein sequences
    protein_id = db.Column(db.String(32), db.ForeignKey('sequences.id'), nullable=True)
    nuc_seqs = db.relationship('Sequence', remote_side=[protein_id], uselist=True)

    @hybrid_property
    def seq(self):
        return self._seq
    @seq.setter
    def seq(self, data):
        self._seq = data.upper()
        self.id = self.to_id(data)
        # self._is_protein = utils.is_protein(data)

    @staticmethod
    def to_id(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def __repr__(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # truncate long values
        for k in ['data', 'error']:
            if d[k] and len(d[k]) > 25:
                d[k] = d[k][:10] + '...' + d[k][-10:]
        return json.dumps(d, default=str)

# class Score(db.Model):
#     __tablename__ = 'scores'
#     sequence_id = db.Column(db.String(32), db.ForeignKey(Sequence.id), primary_key=True, nullable=False)
#     predictor_id = db.Column(db.Integer, db.ForeignKey(Predictor.id), primary_key=True, nullable=False)
#     id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True)
#     score = db.Column(db.Float, nullable=True)
#     data = db.Column(db.Text, nullable=True)
#     error = db.Column(StrippedString(100), nullable=True)

#     batches = db.relationship('Batch', secondary=batch_score, backref='score')

#     def __repr__(self):
#         return json.dumps({c.name: getattr(self, c.name) for c in self.__table__.columns}, default=str)

# class Family(db.Model):
#    pfam_id = db.Column
