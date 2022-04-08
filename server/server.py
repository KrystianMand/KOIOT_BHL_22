from unicodedata import name
from flask import Flask, Response, request
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
def add_visit(number_of_points, date, person_id, place_id):
    visit = Visits(number_of_points=number_of_points, date=date, person_id=person_id, place_id=place_id)
    db.session.add(visit)
    db.session.commit()

def add_task_done(number_of_points, date, person_id, place_id):
    task = Tasks_done(number_of_points=number_of_points, date=date, person_id=person_id, place_id=place_id)
    db.session.add(task)
    db.session.commit()
    
class PersonData(Resource):
    def get(self, id):
        # Do stuff with id 
        person = Person.query.filter_by(id=id).all()
        print(person)
        if person:
            visitPoint = Visits.query.filter_by(person_id=id).all()
            taskPoint = Tasks_done.query.filter_by(person_id=id).all()
            points = 0
            for visit in visitPoint:
                points += visit.number_of_points
            for task in taskPoint:
                points += task.number_of_points
            data = {"id": id, "name": person[0].name, "surname": person[0].surname, "points": points}
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
        # print(type(place))
        if place:
            # if Visits.query.filter_by(id=args.person_id):
            today = str(datetime.today().date())
            visits = Visits.query.filter_by(person_id=args.person_id, place_id=args.place_id).all()
            print(visits[-1].date)
            # splitted_visit = visits[-1].date.split(' ')
            # day_of_visit = splitted_visit[0]
            if visits:
                if visits[-1].date == today: # Last element in the list (date of last visit)
                    return {"is_exist": True, "is_visited": True}
                else:
                    add_visit(number_of_points=1, date=today, person_id=args.person_id, place_id=args.place_id) # Dodanie kolejnej wizyty
                    print("Tu")
                    return {"is_exist": True, "is_visited": False}
            else:
                add_visit(number_of_points=1, date=today, person_id=args.person_id, place_id=args.place_id) # Dodanie pierwszej wizyty
                return {"is_exist": True, "is_visited": False} # Lista wizyt (w tym miejscu) jest pusta, pierwsza wizyta
        else:
            return {"is_exist": False, "is_visited": False} # Miejsce nie istnieje

class Task(Resource):
    def __init__(self):
        self.args_parser = reqparse.RequestParser()
        
        self.args_parser.add_argument(name='task_id', required=True)
        self.args_parser.add_argument(name='person_id', required=True)
        self.args_parser.add_argument(name='place_id', required=True)
        
    def post(self):
        args = self.args_parser.parse_args()
        place = Places.query.filter_by(id=args.place_id)
        if place:
            today = str(datetime.today().date())
            tasks = Tasks_done.query.filter_by(person_id=args.person_id, place_id=args.place_id).all()
            if tasks:
                if tasks[-1].date == today: # Last element in the list (date of last visit)
                    return {"is_exist": True, "is_visited": True}
                else:
                    add_task_done(number_of_points=1, date=today, person_id=args.person_id, place_id=args.place_id)
                    return {"is_exist": True, "is_visited": False}
            else:
                add_task_done(number_of_points=1, date=today, person_id=args.person_id, place_id=args.place_id) 
                return {"is_exist": True, "is_visited": False}
        else:
            return {"is_exist": False, "is_visited": False} # Miejsce nie istnieje
        
# api.add_resource(First, '/')
api.add_resource(PersonData, '/person/<id>')
api.add_resource(Visit, '/visit')
api.add_resource(Task, '/task')

if __name__=="__main__":
    app.run(debug=True)