"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

django_application = get_wsgi_application()
django_application = WhiteNoise(django_application, root=settings.STATIC_ROOT)


def https_app(environ, start_response):
    environ["wsgi.url_scheme"] = "https"
    return django_application(environ, start_response)


application = https_app
