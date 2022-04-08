from flask import Flask

app = Flask(__name__)

state = {
    'level': 50
}

@app.route("/")
def home():
    return state

if __name__=="__main__":
    app.run()