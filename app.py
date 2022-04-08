import email
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(30))

@app.route("/")
def index():
    data_list=User.query.all()
    print(data_list)
    return render_template("index.html")
@app.route("/add")
def add():
    # add new item
    admin = User(username="michaltyczynski", email="m.tyczynski1993@gmail.com", password="lolek1200")
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    
    app.run(debug=True)