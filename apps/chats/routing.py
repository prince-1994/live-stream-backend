from django.urls import re_path
from . import consumers
from channels.routing import URLRouter
from apps.chats.token_auth import TokenAuthMiddleware
from channels.security.websocket import AllowedHostsOriginValidator


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<show_id>\w+)/$", consumers.ShowConsumer.as_asgi()),
]

application = AllowedHostsOriginValidator(
    TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
)
application = TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
