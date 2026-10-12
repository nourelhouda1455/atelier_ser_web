"""
ASGI config for gestion_grandeurs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
import os,django 
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from dashboard.routing import websocket_urlpatterns
from mqtt_topics.consumers import MyMqttConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_grandeurs.settings')

django.setup()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'mqtt': MyMqttConsumer.as_asgi(),
    'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})
