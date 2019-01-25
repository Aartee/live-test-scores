from django.conf.urls import include, url
import django_eventstream
from . import views

urlpatterns = [
	url(r'^students/(?P<id>\w{0,50})/$', views.studentTestScores),
	url(r'^exams/(?P<number>[0-9]+)/$', views.examScores),
]
