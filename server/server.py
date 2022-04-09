from flask import Flask
from flask_restful import Api
from db import db_init
from resources import PersonData, Visit, Task

app = Flask(__name__)
api = Api(app)

# HOST = '192.168.43.145'
HOST = 'localhost'

# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)
        
api.add_resource(PersonData, '/person/<id>')
api.add_resource(Visit, '/visit')
api.add_resource(Task, '/task')

if __name__=="__main__":
    app.run(host=HOST, debug=True)