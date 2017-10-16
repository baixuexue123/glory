"""
WSGI config for glory project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glory.settings")

application = get_wsgi_application()
