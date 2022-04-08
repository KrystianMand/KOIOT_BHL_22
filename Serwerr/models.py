from db import db


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    visit = db.relationship("Visits", primaryjoin="Person.id==Visits.person_id",
    backref='person', lazy=True)
    task_done = db.relationship("Tasks_done",primaryjoin="Person.id==Tasks_done.person_id",
     backref='person', lazy=True)

class Places(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    cords = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    visit = db.relationship("Visits",primaryjoin="Places.id==Visits.place_id",
     backref='place', lazy=True)
    task_done = db.relationship("Tasks_done",primaryjoin="Places.id==Tasks_done.place_id",
     backref='place', lazy=True)

# ids = db.Table('ids',
#     db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False),
#     db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
# )
class Visits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_points = db.Column(db.Integer, unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
class Tasks_done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_points =  db.Column(db.Integer, unique=True, nullable=False)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    person_id = db.Column(db.Integer,db.ForeignKey('person.id'), nullable=False)
    place_id = db.Column(db.Integer,db.ForeignKey('place.id'), nullable=False)