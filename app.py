from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from serverless_wsgi import handle_request
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")

# Initialize database only in development
if os.getenv("FLASK_ENV") == "development":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/flask_todo_py"
    )
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

    with app.app_context():
        db.create_all()
else:
    # In-memory task storage for production
    class Task:
        def __init__(self, id, title, description, completed=False):
            self.id = id
            self.title = title
            self.description = description
            self.completed = completed
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        def __repr__(self):
            return f"<Task {self.id}>"


# Global in-memory storage for production
tasks = []
task_id_counter = 1


def create_sample_todos():
    sample_todos = [
        {
            "title": "Complete Project Setup",
            "description": "Set up Flask project with PostgreSQL and SQLAlchemy",
        },
        {
            "title": "Design Database Schema",
            "description": "Create and implement database models for the todo app",
        },
        {
            "title": "Implement User Interface",
            "description": "Create responsive UI using Bootstrap",
        },
        {
            "title": "Add Authentication",
            "description": "Implement user login and registration system",
        },
        {
            "title": "Write API Documentation",
            "description": "Document all API endpoints and their usage",
        },
        {
            "title": "Add Unit Tests",
            "description": "Write test cases for all major functionality",
        },
        {
            "title": "Deploy Application",
            "description": "Deploy the application to production server",
        },
        {
            "title": "Monitor Performance",
            "description": "Set up monitoring and logging for the application",
        },
        {
            "title": "Backup Database",
            "description": "Implement automated database backup system",
        },
        {
            "title": "Update Dependencies",
            "description": "Update all project dependencies to latest versions",
        },
    ]

    if os.getenv("FLASK_ENV") == "development":
        for todo in sample_todos:
            task = Task(**todo)
            db.session.add(task)
        db.session.commit()
    else:
        global task_id_counter
        for todo in sample_todos:
            task = Task(task_id_counter, **todo)
            tasks.append(task)
            task_id_counter += 1


# Initialize sample todos if empty
if os.getenv("FLASK_ENV") == "development":
    with app.app_context():
        if Task.query.count() == 0:
            create_sample_todos()
else:
    if not tasks:
        create_sample_todos()


# Handle requests from Vercel
def handler(event, context):
    return handle_request(app, event, context)


@app.route("/", methods=["GET", "POST"])
def index():
    if os.getenv("FLASK_ENV") == "development":
        todos = Task.query.order_by(Task.created_at.desc()).all()
    else:
        todos = sorted(tasks, key=lambda x: x.created_at, reverse=True)
    return render_template("index.html", todos=todos)


@app.route("/todos/new", methods=["GET", "POST"])
def new_todo():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        completed = True if request.form.get("completed") == "1" else False

        if os.getenv("FLASK_ENV") == "development":
            todo = Task(title=title, description=description, completed=completed)
            db.session.add(todo)
            db.session.commit()
        else:
            global task_id_counter
            todo = Task(task_id_counter, title, description, completed)
            tasks.append(todo)
            task_id_counter += 1

        flash("Todo added successfully", "success")
        return redirect(url_for("index"))
    return render_template(
        "index.html",
        action="new",
        todo=(
            Task(0, "", "", False)
            if os.getenv("FLASK_ENV") != "development"
            else Task(title="", description="", completed=False)
        ),
    )


@app.route("/delete-todo/<int:id>")
def delete_todo(id):
    if os.getenv("FLASK_ENV") == "development":
        todo = Task.query.get(id)
        db.session.delete(todo)
        db.session.commit()
    else:
        global tasks
        tasks = [task for task in tasks if task.id != id]
    flash("Todo deleted successfully", "success")
    return redirect(url_for("index"))


@app.route("/todos/edit/<int:id>", methods=["GET", "POST"])
def edit_todo(id):
    if os.getenv("FLASK_ENV") == "development":
        todo = Task.query.get_or_404(id)
    else:
        todo = next((task for task in tasks if task.id == id), None)
        if todo is None:
            flash("Todo not found", "error")
            return redirect(url_for("index"))

    if request.method == "POST":
        todo.title = request.form["title"]
        todo.description = request.form["description"]
        todo.completed = True if request.form.get("completed") == "1" else False
        todo.updated_at = datetime.now()

        if os.getenv("FLASK_ENV") == "development":
            db.session.commit()

        flash("Todo updated successfully", "success")
        return redirect(url_for("index"))
    return render_template("index.html", action="edit", todo=todo)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.run(debug=True, port=8000)
    else:
        app.run()
