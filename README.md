# Anomaly Detection Project

A Django-based web application for real-time anomaly detection using temperature sensor data.

## Features

- User authentication (signup/login)
- Real-time temperature data streaming
- Anomaly probability prediction via external ML API
- Alert system for critical anomalies
- Responsive web interface

## Project Structure

```
anomaly_project/
├── db.sqlite3                    # SQLite database file
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── config/                       # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
└── detector/                     # Main Django app
    ├── __init__.py
    ├── admin.py                  # Django admin configuration
    ├── apps.py                   # App configuration
    ├── forms.py                  # Django forms (login/signup)
    ├── models.py                 # Database models (User)
    ├── tests.py                  # Unit tests
    ├── urls.py                   # App URL patterns
    ├── views.py                  # View functions
    ├── migrations/               # Database migrations
    │   ├── __init__.py
    │   └── 0001_initial.py       # Initial migration
    └── templates/                # HTML templates
        └── detector/
            ├── home.html         # Main dashboard
            ├── home1.html        # Alternative dashboard
            ├── login.html        # Login page
            └── signup.html       # Signup page
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd anomaly_project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://localhost:8000`
2. Sign up or log in
3. Start streaming temperature data
4. View anomaly predictions and alerts

## Configuration

- The ML prediction API is hosted at `https://maximum-unzip-goggles.ngrok-free.dev/predict`
- Alerts are sent via email when anomaly probability exceeds 70%
- Ensure the external API is accessible for predictions to work

## Requirements

- Python 3.8+
- Django 4.0+
- See `requirements.txt` for full dependencies

## Troubleshooting

- If predictions fail, check connectivity to the external ML API
- Ensure virtual environment is activated
- Check Django logs for detailed error messages