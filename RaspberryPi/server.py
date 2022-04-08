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
# --------------------------------- database -------------------------------------------

state = {    
    # 1: {                                                                      
    #     'green' : 0,
    #     'blue' : 50,
    #     'red' : 90
    # },
    # 2: {                                                                       
    #     'green' : 10,
    #     'blue' : 20,
    #     'red' : 30
    # }
}




# --------------------------------- index site ------------------------------------------


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

# --------------------------------- classes ------------------------------------------

class Login(Resource):                              

    def get(self):

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




# -------- /led --------------------

class LEDControl(Resource):

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                 

    def get(self):
        """ Returns all devices IDs."""
        try:
            return {"devices" : list(state.keys())}
        except:
            return None, 404

    def post(self):
        """Adds new device. Returns new device ID."""
        global state    
        
        if list(state.keys()) != []:
            newID = max(state.keys()) + 1
        else:
            newID = 1

        state[newID] = {}

        logger.info("Added new device - ID: " + str(newID))

        return {"id": newID}


# -------- /led/<dev_id> ------------

class LEDControlID(Resource):

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                 

        self.args_parser.add_argument(
            name='color',  # Name of arguement
            required=True,  # Mandatory arguement
            type=str,                
            help='Set the color of LED',
            default=None)

        self.args_parser.add_argument(
            name='level',  # Name of arguement
            required=True,  # Mandatory arguement
            type=inputs.int_range(0, 100),  # Allowed range 0..100                  
            help='Set LED brightness level {error_msg}',
            default=None)

    def get(self, dev_id):
        """ Returns all colors from <dev_id> device."""  
        try:
            return {"colors" : state[int(dev_id)]}
        except:
            return None, 404


    def post(self, dev_id):
        """Adds new color to <dev_id>. Returns new color's name and it's level."""
        global state    

        args = self.args_parser.parse_args() # level, color

        try:
            if args.color in list(state[int(dev_id)].keys()):
                return "Taki kolor już istnieje!", 409
            state[int(dev_id)][args.color] = args.level
            logger.info("Added new color - ID: " + str(dev_id) + ", color: " + str(args.color) +", level: " + str(args.level))
            return {args.color : args.level}
        except:
            return None, 404

    def delete(self, dev_id):
        """Deletes device <dev_id>."""
        global state    

        try:
            state.pop(int(dev_id))
            logger.info("Deleted device - ID: " + str(dev_id))
            return {}
        except:
            logger.info("ERROR: There is not device - ID: " + str(dev_id))
            return {}, 404



# -------- /led/<dev_id>/<color> ------------

class LEDControlIDColor(Resource):

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                 

        self.args_parser.add_argument(
            name='level',  # Name of argument
            required=True,  # Mandatory argument
            type=inputs.int_range(0, 100),  # Allowed range 0..100                  
            help='Set LED brightness level {error_msg}',
            default=None)

    def get(self, dev_id, color):
        """ Returns <color> level from <dev_id> device."""
        try:
            return {"level" : state[int(dev_id)][color]}
        except:
            return None, 404

    def post(self, dev_id, color):
        """Sets <color> level to <dev_id> device. Returns <color> level from <dev_id> device."""
        global state    

        args = self.args_parser.parse_args() # level, color
        
        try:
            if color not in list(state[int(dev_id)].keys()):
                return None, 404

            state[int(dev_id)][color] = args.level
            return {"level" : state[int(dev_id)][color]}
        except:
            return None, 404


    def delete(self, dev_id, color):
        """Deletes <color> from device <dev_id>."""
        global state    

        try:
            state[int(dev_id)].pop(color)
            logger.info("Deleted color " + str(color) + " from device - ID: " + str(dev_id))
            return {}
        except:
            logger.info("ERROR: There is not " + str(color) + " in device - ID: " + str(dev_id))
            return {}, 404



# ------------------------------------ register URIs ----------------------------------------

# Register Flask-RESTful resource and mount to server end points
api.add_resource(LEDControl, '/v1/led')
api.add_resource(LEDControlID, '/v1/led/<dev_id>') 
api.add_resource(LEDControlIDColor, '/v1/led/<dev_id>/<color>') 
api.add_resource(Login, '/login')                         



# ------------------------------------ run server -------------------------------------------------

if __name__ == '__main__':
    reader = SimpleMFRC522()
    app.run(host="0.0.0.0", debug=True)   
                                             
