from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
from flask_mail import Mail, Message
# import config
import os

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')


app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    # MAIL_USERNAME = config.MAIL_USERNAME,
    # MAIL_PASSWORD = config.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER = 'myemail@testemail.com'
)

heroku = Heroku(app)
db = SQLAlchemy(app)
mail = Mail(app)



@app.route("/email", methods=['POST'])
def index():
    if request.content_type == 'application/json':
        get_data = request.get_json()
        name = get_data.get('name')
        sender = get_data.get('email')
        # recipients = [os.environ.get('MAIL_USERNAME')]
        recipients = [config.MAIL_USERNAME]
        headers = [name, sender] + recipients
        subject = get_data.get('subject')
        message = get_data.get('message')
        body = message + "\n\n" + name
    msg = Message(subject, headers, body)
    print(Message)
    mail.send(msg)
    return jsonify('Message has been sent')




class Current(db.Model):
    __tablename__ = 'currentArtwork'
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(120))
    description = db.Column(db.String)
    img_url = db.Column(db.String)

    def __init__(self, title, description, img_url):
        self.title = title
        self.description = description
        self.img_url = img_url

    def __repr__(self):
        return "<Title %r>" % self.title
        
@app.route("/")
def home():
    return "<h1>Hi from Flask</h1>"

@app.route("/current/input", methods=["POST"])
def current_input():
    if request.content_type == "application/json":
        post_data = request.get_json()
        title = post_data.get("title")
        description = post_data.get("description")
        img_url = post_data.get("img_url") 
        reg = Current(title, description, img_url)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("Something went wrong")

@app.route("/current", methods=["GET"])
def return_current():
    all_current = db.session.query(Current.id, Current.title, Current.description, Current.img_url).all()
    print(all_current)
    return jsonify(all_current)

@app.route("/current/<id>", methods=['GET'])
def return_single_current(id):
    one_current = db.session.query(Current.id, Current.title, Current.description, Current.img_url). filter(Current.id == id).first()
    return jsonify(one_current)

@app.route("/delete_current/<id>", methods=["DELETE"])
def current_delete(id):
    if request.content_type == "application/json":
        record = db.session.query(Current).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("completed Delete action")
    return jsonify("Delete failed")

@app.route("/update_current/<id>", methods=["PUT"])
def current_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get("title")
        description = put_data.get("description")
        img_url = put_data.get("img_url")
        record = db.session.query(Current).get(id)
        record.title = title
        record.description = description
        record.img_url = img_url
        db.session.commit()
        return jsonify("Completed Update")
    return jsonify("Failed Update")


    
class Past(db.Model):
    __tablename__ = "pastArtwork" 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(120))
    description = db.Column(db.String)
    img_url = db.Column(db.String)

    def __init__(self, title, description, img_url):
        self.title = title
        self.description = description
        self.img_url = img_url

    def __repr__(self):
        return "<Title %r>" % self.title 


@app.route("/past/input", methods=["POST"])
def past_input():
    if request.content_type == "application/json":
        post_data = request.get_json()
        title = post_data.get("title")
        description = post_data.get("description")
        img_url = post_data.get("img_url")
        reg = Past(title, description, img_url)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("Something went wrong")

@app.route("/past", methods=["GET"])
def return_past():
    all_past = db.session.query(Past.id, Past.title, Past.description, Past.img_url).all()
    return jsonify(all_past)

@app.route("/past/<id>", methods=['GET'])
def return_single_past(id):
    one_past = db.session.query(Past.id, Past.title, Past.description, Past.img_url). filter(Past.id == id).first()
    return jsonify(one_past)

@app.route("/delete_past/<id>", methods=["DELETE"])
def past_delete(id):
    if request.content_type == "application/json":
        record = db.session.query(Past).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("completed Delete action")
    return jsonify("Delete failed")

@app.route("/update_past/<id>", methods=["PUT"])
def past_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get("title")
        description = put_data.get("description")
        img_url = put_data.get("img_url")
        record = db.session.query(Past).get(id)
        record.title = title
        record.description = description
        record.img_url = img_url
        db.session.commit()
        return jsonify("Completed Update")
    return jsonify("Failed Update")

if __name__ == "__main__":
    app.debug = True
    app.run()