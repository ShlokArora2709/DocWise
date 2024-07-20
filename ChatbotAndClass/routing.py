from django.urls import re_path
import ChatbotAndClass.consumers as consumers

websocket_urlpatterns = [
    re_path(r'wss/videocall/(?P<room_name>[^/]+)/$', consumers.VideoCallConsumer.as_asgi()),
    re_path(r'ws/videocall/(?P<room_name>[^/]+)/$', consumers.VideoCallConsumer.as_asgi()),
]