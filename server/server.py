from unicodedata import name
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class PersonId(Resource):
    def get(self, id):
        print(id)  
        
        return {"person": "id"}
    
class Visit(Resource):
    def __init__(self):
        self.args_parser = reqparse.RequestParser()
        
        self.args_parser.add_argument(name='person_id', required=True)
        self.args_parser.add_argument(name='place_id', required=True)
        
    def post(self):
        args = self.args_parser.parse_args()
        
        return "OK"   

class Task(Resource):
    def __init__(self):
        self.args_parser = reqparse.RequestParser()
        
        self.args_parser.add_argument(name='task_id', required=True)
        self.args_parser.add_argument(name='person_id', required=True)
        
    def post(self):
        args = self.args_parser.parse_args()
        
        return "OK"
        
    
api.add_resource(PersonId, '/person/<id>')
api.add_resource(Visit, '/visit')
api.add_resource(Task, '/task')

if __name__=="__main__":
    app.run(debug=True)