# Clinic Appointment System - Setup Guide

This guide will help you set up and run the Django Clinic Appointment System project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (Python 3.13 is recommended)
- **pip** (Python package installer)
- **pipenv** (Python package and virtual environment manager)
- **Git** (for version control)

You can verify your installations by running:

```bash
python --version
pip --version
pipenv --version
git --version
```

### Install pipenv (if not installed)

```bash
pip install pipenv
```

## Step 1: Clone the Repository

If you haven't already, clone or navigate to the project directory:

```bash
cd clinic-appointment-system
```

## Step 2: Install Dependencies with Pipenv

This project uses **pipenv** for dependency management. Pipenv automatically creates and manages a virtual environment for you.

Install all dependencies (this will also create the virtual environment):

```bash
pipenv install
```

This command will:

- Create a virtual environment automatically (if it doesn't exist)
- Install Django 5.2.8 and all its dependencies from `Pipfile`
- Generate/update `Pipfile.lock` with exact dependency versions

**Important:** Both `Pipfile` and `Pipfile.lock` should be committed to version control:

- `Pipfile` - Defines your project dependencies (like `requirements.txt`)
- `Pipfile.lock` - Locks exact versions for reproducible builds across all environments

**Current dependencies:**

- Django 5.2.8
- sqlparse (Django dependency, automatically installed)
- asgiref (Django dependency, automatically installed)
- tzdata (Django dependency, automatically installed)

## Step 4: Environment Variables

Create a `.env` file in the project root directory (if not already present):

```bash
# In the project root (clinic-appointment-system/)
touch .env
```

Add the following environment variables to `.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Note:** This project uses SQLite as the database, which requires no additional configuration. The database file (`db.sqlite3`) will be created automatically when you run migrations.

**Important:**

- Generate a new secret key for production. You can use Django's secret key generator:
  ```bash
  pipenv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Never commit the `.env` file to version control (it's already in `.gitignore`)

## Step 5: Configure Django Settings

The project settings are located in `clinic_project/clinic_project/settings.py`.

**Key settings to review:**

- `SECRET_KEY`: Should be loaded from environment variables in production
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain in production

**Database Configuration:**

This project uses **SQLite**, which is perfect for development and small to medium-sized applications. SQLite:

- Requires no separate database server installation
- Stores data in a single file (`db.sqlite3`)
- Is automatically created when you run migrations
- Works out of the box with Django

No additional database configuration is needed!

## Step 6: Database Setup

Since we're using SQLite, no database server setup is required. The database file will be created automatically.

### Run Migrations

Apply database migrations to create the necessary tables and the SQLite database file:

Run from the project root using the full path:

```bash
pipenv run python clinic_project/manage.py migrate
```

This will:

- Create the `db.sqlite3` file in the `clinic_project/` directory
- Create all necessary database tables:
  - Django admin tables
  - Authentication tables
  - Session tables
  - Content types
  - And other default Django tables

**Note:** The `db.sqlite3` file is already in `.gitignore` and won't be committed to version control.

### Create Superuser (Admin Account)

Create an admin user to access the Django admin panel:

```bash
pipenv run python clinic_project/manage.py createsuperuser
```

Follow the prompts to enter:

- Username
- Email address (optional)
- Password

## Step 7: Run the Development Server

Start the Django development server:

```bash
pipenv run python clinic_project/manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

You can also specify a different port:

```bash
pipenv run python clinic_project/manage.py runserver 8080
```

### Access Points

- **Home/App URLs**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## Step 8: Verify Installation

1. Open your browser and navigate to `http://127.0.0.1:8000/`
2. You should see the Django welcome page or your app's homepage
3. Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials

**Note:** The virtual environment is managed by pipenv and stored outside the project directory (typically in your user's home directory under `.virtualenvs/`).

## Common Commands

### Pipenv Commands

```bash
# Install all dependencies
pipenv install

# Install a new package
pipenv install <package-name>

# Install a development package
pipenv install --dev <package-name>

# Run a command in the virtual environment
pipenv run <command>

# Show dependency graph
pipenv graph

# Update all dependencies
pipenv update

# Update a specific package
pipenv update <package-name>

# Check for security vulnerabilities
pipenv check

# Show virtual environment path
pipenv --venv
```

### Django Commands (using pipenv)

All Django commands should be prefixed with `pipenv run` and use the full path to `manage.py`:

#### Database Operations

```bash
# Create migrations for model changes
pipenv run python clinic_project/manage.py makemigrations

# Apply migrations
pipenv run python clinic_project/manage.py migrate

# Show migration status
pipenv run python clinic_project/manage.py showmigrations
```

#### User Management

```bash
# Create superuser
pipenv run python clinic_project/manage.py createsuperuser

# Change user password
pipenv run python clinic_project/manage.py changepassword <username>
```

#### Development

```bash
# Run development server
pipenv run python clinic_project/manage.py runserver

# Run development server on specific port
pipenv run python clinic_project/manage.py runserver 8080

# Run development server accessible from network
pipenv run python clinic_project/manage.py runserver 0.0.0.0:8000
```

#### Django Shell

```bash
# Open Django shell (Python shell with Django context)
pipenv run python clinic_project/manage.py shell

# Open Django shell with IPython (if installed)
pipenv run python clinic_project/manage.py shell -i ipython
```

#### Static Files

```bash
# Collect static files for production
pipenv run python clinic_project/manage.py collectstatic
```

#### Testing

```bash
# Run all tests
pipenv run python clinic_project/manage.py test

# Run tests for specific app
pipenv run python clinic_project/manage.py test clinic_app

# Run specific test
pipenv run python clinic_project/manage.py test clinic_app.tests.TestClassName
```

## Troubleshooting

### Issue: `pipenv: command not found`

**Solution:** Install pipenv:

```bash
pip install pipenv
```

### Issue: `ModuleNotFoundError: No module named 'django'`

**Solution:** Make sure dependencies are installed:

```bash
pipenv install
```

If the issue persists, ensure you're using `pipenv run` before all commands.

### Issue: `can't open file 'manage.py': [Errno 2] No such file or directory`

**Solution:** Run from the project root using the full path to `manage.py`:

```bash
pipenv run python clinic_project/manage.py migrate
```

### Issue: `django.db.utils.OperationalError: no such table`

**Solution:** Run migrations:

```bash
pipenv run python clinic_project/manage.py migrate
```

### Issue: `Port already in use`

**Solution:** Use a different port:

```bash
pipenv run python clinic_project/manage.py runserver 8080
```

### Issue: `SECRET_KEY` error

**Solution:** Make sure you have a `.env` file with `SECRET_KEY` set, or update `settings.py` to use environment variables.

### Issue: Cannot access admin panel

**Solution:**

1. Make sure you've created a superuser: `pipenv run python clinic_project/manage.py createsuperuser`
2. Check that migrations have been applied: `pipenv run python clinic_project/manage.py migrate`

### Issue: Pipfile.lock is out of date

**Solution:** Update the lockfile:

```bash
pipenv lock
```

Or update dependencies and lockfile:

```bash
pipenv update
```

### Issue: Virtual environment not found

**Solution:** Reinstall dependencies:

```bash
pipenv install
```

This will recreate the virtual environment if needed.

## Next Steps

1. **Create Models**: Define your database models in `clinic_app/models.py`
2. **Create Views**: Add view functions/classes in `clinic_app/views.py`
3. **Configure URLs**: Set up URL patterns in `clinic_app/urls.py` and include them in `clinic_project/urls.py`
4. **Create Templates**: Add HTML templates in `clinic_app/templates/`
5. **Add Static Files**: Add CSS, JavaScript, and images in `clinic_app/static/`
6. **Write Tests**: Add test cases in `clinic_app/tests.py`

---
