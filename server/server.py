from unicodedata import name
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# import json

app = Flask(__name__)
api = Api(app)

class PersonData(Resource):
    def get(self, id):
        # Do stuff with id 
        data = {"id": id, "name": "Marian", "surname": "Jakies nazwisko"}
        # json_data = json.dumps(data)
        return data
    
class Visit(Resource):
    def __init__(self):
        self.args_parser = reqparse.RequestParser()
        
        self.args_parser.add_argument(name='person_id', required=True)
        self.args_parser.add_argument(name='place_id', required=True)
        
    def post(self):
        args = self.args_parser.parse_args()
        # Do stuff with args
        data = {"is_visited": "true"}
        return data   

class Task(Resource):
    def __init__(self):
        self.args_parser = reqparse.RequestParser()
        
        self.args_parser.add_argument(name='task_id', required=True)
        self.args_parser.add_argument(name='person_id', required=True)
        
    def post(self):
        args = self.args_parser.parse_args()
        # Do stuff with args
        data = {"is_done": "true"}
        return data 
        
    
api.add_resource(PersonData, '/person/<id>')
api.add_resource(Visit, '/visit')
api.add_resource(Task, '/task')

if __name__=="__main__":
    app.run(debug=True)