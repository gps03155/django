# -*- coding: utf-8 -*-
from django.urls import re_path
from . import consumers
from . import consumers_async

websocket_urlpatterns = [
    # sync
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),

    # async
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers_async.ChatConsumer.as_asgi())
]
