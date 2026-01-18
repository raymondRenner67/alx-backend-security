"""
WSGI config for alx-backend-security project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_prod')

application = get_wsgi_application()
