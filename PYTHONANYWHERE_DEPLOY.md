# PythonAnywhere Deployment Guide

## Step 1: Upload Your Code

1. Log in to PythonAnywhere: https://www.pythonanywhere.com
2. Go to "Files" tab
3. Upload your code or clone from GitHub:
   ```bash
   cd ~
   git clone https://github.com/your-username/alx-backend-security.git
   cd alx-backend-security
   ```

## Step 2: Create Virtual Environment

```bash
cd ~/alx-backend-security
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

Create a `.env` file:
```bash
nano .env
```

Add your environment variables (see .env.example)

## Step 4: Setup Database

```bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=settings_prod
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Step 5: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose Python 3.11
5. Set source code directory: `/home/yourusername/alx-backend-security`
6. Set working directory: `/home/yourusername/alx-backend-security`

## Step 6: Configure WSGI File

Edit the WSGI configuration file:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/alx-backend-security'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_prod'

# Load environment variables from .env file
from pathlib import Path
from decouple import config

# Activate virtual environment
activate_this = '/home/yourusername/alx-backend-security/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 7: Configure Static Files

In the "Web" tab, under "Static files":
- URL: `/static/`
- Directory: `/home/yourusername/alx-backend-security/staticfiles/`

## Step 8: Setup Celery (Using Always-On Task)

**Note:** PythonAnywhere free tier doesn't support long-running processes.
For Celery, you'll need a paid plan.

If you have a paid plan:

1. Create a bash script `start_celery.sh`:
```bash
#!/bin/bash
cd /home/yourusername/alx-backend-security
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=settings_prod

# Start Celery worker
celery -A celery worker --loglevel=info &

# Start Celery beat
celery -A celery beat --loglevel=info &
```

2. Make it executable:
```bash
chmod +x start_celery.sh
```

3. Add to "Always-on tasks" in the "Tasks" tab

## Step 9: Reload Web App

Click the green "Reload" button on the Web tab

## Testing

Your app will be available at:
- Main site: `https://yourusername.pythonanywhere.com`
- Swagger: `https://yourusername.pythonanywhere.com/swagger/`
- Admin: `https://yourusername.pythonanywhere.com/admin/`

## Limitations on Free Tier

1. No outbound internet access (geolocation API won't work)
2. No long-running processes (Celery won't work)
3. CPU time limits

**Recommendation:** Use Render.com for full feature support including Celery and RabbitMQ.
