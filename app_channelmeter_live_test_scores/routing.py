from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream

urlpatterns = [
    url(r'^events/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['test']}),

    url(r'^students/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['students_channel']}),

    url(r'^exams/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['exams']}),

    url(r'', AsgiHandler),
]
