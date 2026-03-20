"""
WSGI config for Phoenix Epoch project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phoenix_epoch.settings.dev")

application = get_wsgi_application()
