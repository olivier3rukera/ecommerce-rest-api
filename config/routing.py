from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#from toraxnet.offers.consumers import ChatConsumer
application = ProtocolTypeRouter({
    'websocket':
        URLRouter([
           # path('ws/chat/<uuid:room_uuid>/<uuid:user_id>/', ChatConsumer),
           # path('/ws/chat/<uuid:room_uuid>/<uuid:user_id>/', ChatConsumer)
        ])


})
