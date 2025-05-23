"""
ASGI config for marva project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

import core.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marva.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles regular HTTP requests
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                core.routing.websocket_urlpatterns  # Your WebSocket URLs
            )
        )
    ),
})
