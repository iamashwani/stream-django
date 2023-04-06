from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import LiveStreamConsumer



application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("/ws/live/", LiveStreamConsumer.as_asgi()),
    ]),
})
