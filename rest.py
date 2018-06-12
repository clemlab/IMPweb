"""Provide an API
https://flask-restful.readthedocs.io/en/latest/quickstart.html
"""

from flask_restful import Resource, Api, reqparse

parser = reqparse.RequestParser()
parser.add_argument('secret_key', type=int, help='Client secret key for the request')
args = parser.parse_args()

# must always put the secret
class ScoreSequenceBatch(Resource):
    # retrieve with user_payload and batch id
    # retrieve with batch_payload
    # retrieve all batches
    # options to get all data for each sequence, or just the score
    # json delimited response
    def get(self, todo_id):
        pass
    # delete only works if sequence has not yet been run
    # only if we can figure this out of RQ (if possible to go through rq queue)
    def delete(self, todo_id):
        return '', 204

    # def put(self, todo_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     TODOS[todo_id] = task
    #     return task, 201

    # submit sequences
    # return batch id and batch_payload
    def post(self):
        args = parser.parse_args()
        args['task']
        return TODOS[todo_id], 201
