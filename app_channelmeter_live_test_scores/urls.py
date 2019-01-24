from django.conf.urls import include, url
import django_eventstream
from . import views

urlpatterns = [
	# url(r'^students/$', views.students),
	# url(r'^students/$', include(django_eventstream.urls), {'channels': ['students_channel']}),

	url(r'^students/(?P<id>\w{0,50})/$', views.studentTestScores),
	# url(r'^exams/$', views.exams),
	url(r'^exams/(?P<number>[0-9]+)/$', views.examScores),
]
