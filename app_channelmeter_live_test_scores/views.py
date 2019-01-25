import time
import threading
import datetime
from django.shortcuts import render
from django_eventstream import get_current_event_id, send_event
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse
import requests
import sseclient
import json
import collections

def _inmemory_live_test_scores_worker():
	url = "http://live-test-scores.herokuapp.com/scores"
	response = requests.get(url, stream = True)
	client = sseclient.SSEClient(response)

	for event in client.events():
		data = json.loads(event.data)
		global_live_test_scores[data["studentId"]].append([data["exam"], data["score"]])
		global_exams[data["exam"]].append([data["studentId"], data["score"]])
		send_event('test', 'score', data)

def students():
    while True:
        studentList = {}
        studentList["studentList"] = [student for student, value in global_live_test_scores.items() if len(value) >= 1]
        send_event("students_channel", 'students', studentList)

def stream_studentTestScores(id):
	while True:
		test_scores = {}
		try:
			test_scores["test_results"] = global_live_test_scores[id]
			test_scores["average_score"] = sum(test[1] for test in global_live_test_scores[id]) / len(global_live_test_scores[id])
		except:
			exception_msg = "student " + id + " does not exist. Please try providing one of the students from list of students in http://localhost:8000/students/"
			test_scores["Exception"] = exception_msg
			print(exception_msg)

		time.sleep(1)
		yield json.dumps(test_scores)

def studentTestScores(request, id):
	stream = stream_studentTestScores(id)		
	response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
	response['Cache-Control'] = 'no-cache'
	return response

def exams():
	while True:
		exams = {}
		exams["exams"] = list(global_exams.keys())
		send_event("exams", 'exams', exams)

def stream_examScores(number):
	while True:

		exam_scores = {}

		try:
			number = int(number)
			exam_scores["exam_results"] = global_exams[number]
			exam_scores["average_score"] = sum(exam[1] for exam in global_exams[number]) / len(global_exams[number])
		except:
			exception_msg = "test number " + number + " does not exist. Please try providing one of the test numbers from list of exams in http://localhost:8000/exams/"
			exam_scores["Exception"] = exception_msg
			print(exception_msg)

		time.sleep(2) 
		yield json.dumps(exam_scores)

def examScores(request, number):
	stream = stream_examScores(number)	
	response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
	response['Cache-Control'] = 'no-cache'
	return response

global_live_test_scores = collections.defaultdict(list)
global_exams = collections.defaultdict(list)

inmemory_live_test_scores_thread = threading.Thread(target = _inmemory_live_test_scores_worker)
inmemory_live_test_scores_thread.daemon = True
inmemory_live_test_scores_thread.start()

students_thread = threading.Thread(target = students)
students_thread.daemon = True
students_thread.start()

exams_thread = threading.Thread(target = exams)
exams_thread.daemon = True
exams_thread.start()