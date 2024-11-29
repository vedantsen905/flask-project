
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

if sys.platform != 'win32':  # Check if not on Windows
        import fcntl
else:
        # Define a no-op (empty) function for Windows
        def fcntl(*args, **kwargs):
            pass  # Windows does not support fcntl
    # Define the app and configure it
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
db = SQLAlchemy(app)

    # Define the database model
class Todo(db.Model):
        sno = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        desc = db.Column(db.String(500), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self) -> str:
            return f"Todo('{self.sno}', '{self.title}', '{self.desc}')"

    # Define routes
@app.route("/", methods=['GET', 'POST'])
def hello_world():
        if request.method == 'POST':
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
        allTodo = Todo.query.all()
        return render_template("index.html", allTodo=allTodo)


@app.route("/about")
def about():
        return render_template("about.html")


@app.route("/show")
def show():
        all_todo = Todo.query.all()
        return render_template("index.html", allTodo=all_todo)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
        if request.method == "POST":
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo.query.filter_by(sno=sno).first()  # Corrected here
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            return redirect("/")

        todo = Todo.query.filter_by(sno=sno).first()  # Corrected here
        return render_template("update.html", todo=todo)  # Pass 'todo' here to match template


@app.route("/delete/<int:sno>")
def delete(sno):
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")

    # Create database tables before running the app
if __name__ == "__main__":
        with app.app_context():  # app must be defined before this line
            db.create_all()
            app.run(debug=True , port= 8000)


