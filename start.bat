@echo off
REM Quick Start Script for Windows

echo =====================================
echo ALX Backend Security - Quick Start
echo =====================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env with your configuration
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Run migrations
echo Running migrations...
set DJANGO_SETTINGS_MODULE=settings_prod
python manage.py migrate

REM Ask about superuser
set /p create_superuser="Do you want to create a superuser? (y/n): "
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Print instructions
echo.
echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo To start the application:
echo.
echo 1. Terminal 1 - Django Server:
echo    python manage.py runserver --settings=settings_prod
echo.
echo 2. Terminal 2 - Celery Worker:
echo    celery -A celery worker --loglevel=info
echo.
echo 3. Terminal 3 - Celery Beat:
echo    celery -A celery beat --loglevel=info
echo.
echo Access the application:
echo   - Main app: http://localhost:8000
echo   - Swagger: http://localhost:8000/swagger/
echo   - Admin: http://localhost:8000/admin/
echo.
echo =====================================

pause
