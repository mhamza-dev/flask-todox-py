from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@localhost:5432/flask_todo_py"
)
app.config["SECRET_KEY"] = secrets.token_hex(16)

# Create database if it doesn't exist
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
if not database_exists(engine.url):
    create_database(engine.url)

db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "Todo"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Task {self.id}>"


def create_sample_todos():
    sample_todos = [
        Task(
            title="Complete Project Setup",
            description="Set up Flask project with PostgreSQL and SQLAlchemy",
        ),
        Task(
            title="Design Database Schema",
            description="Create and implement database models for the todo app",
        ),
        Task(
            title="Implement User Interface",
            description="Create responsive UI using Bootstrap",
        ),
        Task(
            title="Add Authentication",
            description="Implement user login and registration system",
        ),
        Task(
            title="Write API Documentation",
            description="Document all API endpoints and their usage",
        ),
        Task(
            title="Add Unit Tests",
            description="Write test cases for all major functionality",
        ),
        Task(
            title="Deploy Application",
            description="Deploy the application to production server",
        ),
        Task(
            title="Monitor Performance",
            description="Set up monitoring and logging for the application",
        ),
        Task(
            title="Backup Database",
            description="Implement automated database backup system",
        ),
        Task(
            title="Update Dependencies",
            description="Update all project dependencies to latest versions",
        ),
    ]

    for todo in sample_todos:
        db.session.add(todo)
    db.session.commit()


with app.app_context():
    db.create_all()
    # Check if database is empty before adding sample todos
    if Task.query.count() == 0:
        create_sample_todos()


@app.route("/", methods=["GET", "POST"])
def index():
    todos = Task.query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", todos=todos)


@app.route("/todos/new", methods=["GET", "POST"])
def new_todo():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        completed = True if request.form.get("completed") == "1" else False
        todo = Task(title=title, description=description, completed=completed)
        db.session.add(todo)
        db.session.commit()
        flash("Todo added successfully", "success")
        return redirect(url_for("index"))
    return render_template(
        "index.html",
        action="new",
        todo=Task(title="", description="", completed=False),
    )


@app.route("/delete-todo/<int:id>")
def delete_todo(id):
    todo = Task.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully", "success")
    return redirect(url_for("index"))


@app.route("/todos/edit/<int:id>", methods=["GET", "POST"])
def edit_todo(id):
    todo = Task.query.get_or_404(id)
    if request.method == "POST":
        print(request.form)
        todo.title = request.form["title"]
        todo.description = request.form["description"]
        todo.completed = True if request.form.get("completed") == "1" else False
        todo.updated_at = datetime.now()
        db.session.commit()
        flash("Todo updated successfully", "success")
        return redirect(url_for("index"))
    return render_template("index.html", action="edit", todo=todo)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
