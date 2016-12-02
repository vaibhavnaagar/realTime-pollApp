from django.conf.urls import url

from ws.views import WebSocketsMainView


urlpatterns = [
    url(r'^inst', WebSocketsMainView.as_view(), name='ws_client'),
    url(r'^stud', WebSocketsMainView.as_view(), name='ws_client'),
]
