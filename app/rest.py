from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from solid_db import *
from ipdb import set_trace as debug

'''RESTFUL API for the Biomonitor.'''
app = Flask(__name__)
CORS(app)
api = Api(app)
db = Solid('data/db.json')


class Sessions(Resource):

    def get(self):
        # Index
        sessions = db.all('sessions')
        return sessions

    def post(self):
        # Create
        data = request.json
        data = db.insert('session', data)
        return data


class Session(Resource):

    def get(self, _id):
        # Index the resource
        data = db.find_by_id(_id)
        return data

    def put(self, _id):
        # Update existing resource
        debug()
        data = request.json
        data = db.update(data)
        return data

    def delete(self, _id):
        # Delete resource
        db.delete(_id)
        return 200


# ADD RESOURCE ROUTES.
api.add_resource(Sessions, '/sessions')
api.add_resource(Session, '/session/<string:_id>')


if __name__ == '__main__':
    app.run(debug=True)

