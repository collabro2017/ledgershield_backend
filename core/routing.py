from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import URLRouter, ProtocolTypeRouter
from django.conf.urls import url
from django.urls import include, path

from v1.transactions.consumers import TransactionConsumer

# application = URLRouter([
#     url(r"^ws/tx/(?P<txid>[^\/]+)$", TransactionConsumer),
#     path('/', include('core.urls'))
#
# ])

application = ProtocolTypeRouter({
    'http': AsgiHandler,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/tx/(?P<txid>[^\/]+)$", TransactionConsumer),
        ])
    )
})
