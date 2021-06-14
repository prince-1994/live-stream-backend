from channels.auth import AuthMiddlewareStack
from django.db.models import query
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(token_key):
    token = Token.objects.get(key=token_key)
    return token.user

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, recieve, send):
        query_string = scope['query_string']
        if query_string :
            try:
                token_name, token_key = query_string.decode().split("=")
                if token_name == 'token':
                    scope['user'] = await get_user(token_key)
                else :
                    scope['user'] = AnonymousUser()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        print(scope['user'])
        return await self.app(scope, recieve, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))