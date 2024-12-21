"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

This script sets up the configuration for a Django project, including logging, environment variables, application settings, and database configuration.

1. **Logging Configuration**:
   - Uses a `RotatingFileHandler` to manage log files with a maximum size of 512 MB.
   - Logs are stored in `file.log`, and up to 5 backup files are maintained.
   - The logging format includes timestamps, log levels, and messages, and the logging level is set to `DEBUG`.

2. **Environment Variables**:
   - The `.env` file is loaded from the parent directory of the project using `dotenv`.
   - Environment variables such as `db_username`, `db_password`, `db_host`, and `db_port` are retrieved for database configuration.
   - Errors during the loading of environment variables are logged.

3. **Django Project Paths**:
   - `BASE_DIR` defines the base directory of the project using `Path`.

4. **Security Settings**:
   - A secret key for Django is hardcoded for development purposes (not recommended for production).
   - Debug mode is enabled (`DEBUG = True`), and the `ALLOWED_HOSTS` list is empty.

5. **Installed Applications**:
   - Includes default Django apps and a custom app named `loyalty_app`.

6. **Middleware**:
   - Configures standard Django middleware for security, session handling, authentication, CSRF protection, and more.

7. **Templates**:
   - Configures the Django template engine with support for application-level templates and standard context processors.

8. **Database Configuration**:
   - Configures a PostgreSQL database with the name `hello_again`.
   - Credentials (`USER`, `PASSWORD`, `HOST`, `PORT`) are dynamically fetched from environment variables.

9. **Password Validation**:
   - Implements default Django password validation rules for security, including similarity checks, minimum length, and common password restrictions.

10. **Internationalization and Localization**:
    - Sets the language to English (`en-us`) and timezone to UTC.
    - Enables internationalization and timezone support.

11. **Static Files**:
    - Defines the URL for serving static files (`STATIC_URL`).

12. **Primary Key Configuration**:
    - Sets the default primary key field type to `BigAutoField`, suitable for large-scale applications.

This script forms the backbone of the Django project's settings and ensures robust logging, secure database access, and proper application behavior.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
max_log_file_size = 512 * 1024 * 1024  # 512 MB

# Build the BASE_DIR path for the project
BASE_DIR = Path(__file__).resolve().parent.parent
logs_path = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(logs_path):
    os.makedirs(logs_path)
env_path = os.path.join(BASE_DIR, ".env")

log_file_path = os.path.join(logs_path, 'settings.log')
handler = RotatingFileHandler(log_file_path, maxBytes=max_log_file_size, backupCount=5)
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler]
)

# Start logging application initialization
logging.info("Initializing Django application settings.")

# Load environment variables
try:
    load_dotenv(dotenv_path=env_path)
    db_username = os.getenv("db_username")
    db_password = os.getenv("db_password")
    db_host = os.getenv("db_host")
    db_port = os.getenv("db_port")
    SECRET_KEY = os.getenv("SECRET_KEY")
    logging.info("Environment variables loaded successfully")
except Exception as e:
    logging.error("Error loading environment variables: %s", e)


# TODO SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'loyalty_app',
]
logging.info(f"Installed apps: {INSTALLED_APPS}")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hello_again.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hello_again.wsgi.application'


# Log database configuration
try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'hello_again',
            'USER': f'{db_username}',
            'PASSWORD': f'{db_password}',
            'HOST': f'{db_host}',
            'PORT': f'{db_port}',
        }
    }
    logging.info("Database configuration loaded successfully.")
    logging.debug(f"Database host: {db_host}, port: {db_port}")
except Exception as e:
    logging.critical("Error configuring database: %s", e)
    raise


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization and localization settings
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
logging.info(f"Static URL set to: {STATIC_URL}")

# Primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
logging.info(f"Default auto field type set to: {DEFAULT_AUTO_FIELD}")

# Finalize logging setup
logging.info("Django application settings initialized successfully.")
