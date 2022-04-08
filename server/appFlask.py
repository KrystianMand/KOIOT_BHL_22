from flask import Flask, request, Response
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Person

app = Flask(__name__)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload():
    name = request.form.get('name')
    surname = request.form.get('surname')
    # pic = request.files['pic']
    # if not pic:
    #     return 'No pic uploaded!', 400

    # filename = secure_filename(pic.filename)
    # mimetype = pic.mimetype #image/jpeg
    # print("pic to: "+ str(pic.read())+ "\n filename to :" +filename)
    # print ("mimetype"+mimetype)
    # if not filename or not mimetype:
    #     return 'Bad upload!', 400

    person = Person(name=name, surname=surname)
    db.session.add(person)
    db.session.commit()

    return 'Img Uploaded!', 200


@app.route('/person/<int:id>')
def get_person(id):
    # img = Img.query.filter_by(id=id).first()
    # if not img:
    #     return 'Img Not Found!', 404
    person= Person.query.get(1)
    return person#Response(img.img, mimetype=img.mimetype)

if __name__ == '__main__':
    app.run(debug=True)
