"""
ASGI config for shopbig project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import django

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from apps.chats.routing import application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": application
})
