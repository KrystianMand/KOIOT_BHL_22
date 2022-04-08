from unicodedata import name
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from db import db_init, db
from models import Person, Visits, Tasks_done, Places
from datetime import datetime
# import json

app = Flask(__name__)
api = Api(app)

# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

# class First(Resource):
#     def get(self):
#         person = Person(name="Marian", surname="Nazwisko")
#         db.session.add(person)
#         db.session.commit()
#         return "OK"
    
class PersonData(Resource):
    def get(self, id):
        # Do stuff with id 
        person = Person.query.get(id)
        if person:
            data = {"id": person.id, "name": person.name, "surname": person.surname}
        else:
            data = {"id": id, "name": "Nie ma", "surname": "Takiego"}
        return data
    
class Visit(Resource):
    def __init__(self):
        self.args_parser = reqparse.RequestParser()
        
        self.args_parser.add_argument(name='person_id', required=True)
        self.args_parser.add_argument(name='place_id', required=True)
        
    def post(self):
        args = self.args_parser.parse_args()
        # Do stuff with args
        place = Places.query.filter_by(id=args.place_id)
        
        if place:
            # if Visits.query.filter_by(id=args.person_id):
            pass
            # today = datetime.today().date()
            # visit = Visits.query.filter_by(id=args.person_id)
            # if visit:
            #     if visit.date.date() == today:
            #         pass
        else:
            pass
        # person = Person(name=name, surname=surname)
        # db.session.add(person)
        # db.session.commit()
        data = {"is_exist": True, "is_visited": True}
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
        
# api.add_resource(First, '/')
api.add_resource(PersonData, '/person/<id>')
api.add_resource(Visit, '/visit')
api.add_resource(Task, '/task')

if __name__=="__main__":
    app.run(debug=True)