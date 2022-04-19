from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lolek1200!@localhost:5432/todo'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

users = {
    "mtyczynski": generate_password_hash("Lolek1200!")
}
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    category = db.Column(db.String(20))
    date = db.Column(db.DateTime)
    complete = db.Column(db.Boolean)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

"""Routes for Customers TODO app functionality include add, modify and delete functions"""

@app.route("/todo")
@auth.login_required
def todo():
    username = users
    todo_list=Todo.query.all()
    print(todo_list)
    return render_template("todo.html", username=username, todo_list=todo_list)

@app.route("/add", methods=['POST'])
def add():
    # add new item
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    new_todo = Todo(title=title, description=description, category=category, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('todo'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo'))

if __name__ == "__main__":
    db.create_all()
    port = os.environ.get("PORT", 5000)
    app.run(debug=True, host='0.0.0.0', port=port)