# Flask Todo Application

A modern, full-featured Todo application built with Flask and PostgreSQL. This application allows users to create, read, update, and delete todo items with a clean and intuitive user interface.

## Features

- Create, read, update, and delete todo items
- Mark todos as complete/incomplete
- Responsive design using Bootstrap
- PostgreSQL database with SQLAlchemy ORM
- Automatic database creation and sample data seeding
- Flash messages for user feedback
- Clean and intuitive user interface

## Prerequisites

- Python 3.x
- PostgreSQL
- pipenv (for dependency management)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd FlaskPractise
```

2. Install dependencies using pipenv:

```bash
pipenv install
```

3. Set up PostgreSQL:

   - Make sure PostgreSQL is running on your system
   - Create a database named `flask_todo_py`
   - Default credentials are:
     - Username: postgres
     - Password: postgres
     - Port: 5432

4. Activate the virtual environment:

```bash
pipenv shell
```

## Running the Application

1. Start the Flask development server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://localhost:8000
```

## Project Structure

```
FlaskPractise/
├── app.py              # Main application file
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── Pipfile           # Python dependencies
└── README.md         # Project documentation
```

## API Endpoints

- `GET /` - Display all todos
- `GET/POST /todos/new` - Create a new todo
- `GET/POST /todos/edit/<id>` - Edit an existing todo
- `GET /delete-todo/<id>` - Delete a todo
- `GET /about` - About page

## Database Schema

The application uses a single table `Todo` with the following columns:

- `id` (Integer, Primary Key)
- `title` (String, Not Null)
- `description` (String, Not Null)
- `completed` (Boolean, Default: False)
- `created_at` (DateTime, Default: Current Time)
- `updated_at` (DateTime, Default: Current Time)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
