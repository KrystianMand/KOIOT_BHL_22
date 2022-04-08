import logging
from flask import Flask, request, render_template, redirect                                  
from flask_restful import Resource, Api, reqparse, inputs   

from mfrc522 import SimpleMFRC522
import json
import requests

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.

# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.                                              
api = Api(app) # Flask-RESTful extension wrapper                                     


class Visitor:
    def __init__(self, is_visited, name, surname, points) -> None:
        self.name = name
        self.surname = surname
        self.points = points

visitor = None


# --------------------------------- sites ------------------------------------------


PLACEID = 1
POSTURI = "http://192.168.43.145:5000/"


data = {"name" : "Adam"}

@app.route('/', methods=['GET'])                                                    
def index():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('index.html')         
    # return 'OK'


@app.route('/dashboard', methods=['GET'])                                                    
def dashboard():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('dashboard.html', visitor = visitor)


@app.route('/play', methods=['GET'])                                                    
def play():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('play.html', visitor = visitor)        

# --------------------------------- classes ------------------------------------------

class Login(Resource):                              

    def get(self):
        global visitor

        rfid, text = reader.read()
        personId = str(rfid)

        # response = requests.post(
        #     POSTURI + "visit", json={"place_id": PLACEID, "person_id": personId}
        # )
        respDict = json.loads(
            '{"is_visited": true,"name": "Marian","surname": "Chleb","points": -1}'
        )  # json.loads(response.content.decode())

        visitor = Visitor(**respDict)

        return redirect("/dashboard", code=302)

class Logout(Resource):                              

    def get(self):
        global visitor

        visitor = None

        return redirect("/", code=302)


class Win(Resource):                              

    def get(self):
        global visitor

        # response = requests.post(
        #     POSTURI + "task", json={"place_id": PLACEID, "person_id": personId}
        # )
        
        # TUTAJ DODAĆ GET AKTUALIZUJĄCY ILOŚĆ PUNKTÓW
        print("Mamy zwycięzcę")

        return redirect("/dashboard", code=302)



# ------------------------------------ register URIs ----------------------------------------

# Register Flask-RESTful resource and mount to server end points
api.add_resource(Login, '/login')  
api.add_resource(Logout, '/logout')    
api.add_resource(Win, '/win')                   



# ------------------------------------ run server -------------------------------------------------

if __name__ == '__main__':
    reader = SimpleMFRC522()
    app.run(host="0.0.0.0", debug=True)   
                                             
