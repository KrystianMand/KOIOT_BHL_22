from datetime import datetime
print ()

def get(self, id):
        # Do stuff with id 
        person = Person.query.filter_by(id=id).all()
        if person:
            visitPoint = Visit.query.filter_by(person_id=id).all()
            taskPoint = Tasks_done.query.filter_by(person_id=id).all()
            points = 0
            for pt in range(len(visitPoint)):
                points+=pt[pt]
            for pt in range(len(taskPoint)):
                points+=pt[pt]
        else:
            data = {"id": id, "name": "Nie ma", "surname": "Takiego"}
        return data